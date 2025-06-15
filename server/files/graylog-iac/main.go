package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"os/exec"
	"slices"
	"strings"
	"syscall"
	"time"

	"github.com/jenswbe/setup/server/graylog-iac/api"
	"github.com/jenswbe/setup/server/graylog-iac/models"
	"golang.org/x/term"
)

func expectedEventDefinitions(inventoryPath string) ([]models.EventDefinition, error) {
	defs := []models.EventDefinition{
		{
			Title:                   "Bjoetiek errors",
			Query:                   `source:eve AND container_name:bjoetiek-frontend AND error AND NOT "No config file found, expecting configuration through ENV variables"`,
			ExecuteEvery:            5 * time.Minute,
			NotificationGracePeriod: 5 * time.Minute,
			SearchWithin:            5 * time.Minute,
		},
		{
			Title:       "Deprecated",
			Description: "Deprecation message found in logs",
			Query: strings.Join([]string{
				`deprecat*`,
				`AND NOT "the capability attribute has been deprecated"`, // Related to KDUMP
				`AND NOT "Calling promisify on a function that returns a Promise is likely a mistake"`,
				`AND NOT "Eavesdropping is deprecated and ignored"`, // Policy to allow eavesdropping in /usr/share/dbus-1/session.conf +33: Eavesdropping is deprecated and ignored
				`AND NOT "EXPERIMENTAL: The journald input is experimental"`,
				`AND NOT "has been deprecated and will be converted on each startup in containerd v2.0"`, // containerd config version `1` has ...
				`AND NOT "loading plugin \"io.containerd.warning.v1.deprecations\"..."`,
				`AND NOT "node --trace-deprecation"`,
				"AND NOT \"`orderBy(..., expr)` is deprecated. Use `orderBy(..., 'asc')` or `orderBy(..., (ob) => ...)` instead\"",
				`AND NOT "pam_env(sshd:session): deprecated reading of user environment enabled"`,
				`AND NOT "Remote repository paths without ssh:// or rclone"`,
				`AND NOT "systemd-udev-settle.service is deprecated. Please fix"`,
				`AND NOT "The collStats command is deprecated."`, // MongoDB
			}, " "),
			ExecuteEvery:            24 * time.Hour,
			NotificationGracePeriod: time.Hour,
			SearchWithin:            24 * time.Hour,
			MappedFields: map[string]string{
				"Message": "source.message",
				"Host":    "source.source",
			},
		},
		{
			Title:                   "Unit-fail-mail errors",
			Description:             "Error in service unit-fail-mail@XXX.service",
			Query:                   "error AND filebeat_systemd_unit:unit-fail-mail*",
			ExecuteEvery:            5 * time.Minute,
			NotificationGracePeriod: 5 * time.Minute,
			SearchWithin:            5 * time.Minute,
			MappedFields: map[string]string{
				"Message": "source.message",
				"Host":    "source.source",
			},
		},
	}

	// Read hosts from inventory
	inventoryHosts, err := getHostsFromInventory(inventoryPath)
	if err != nil {
		return nil, fmt.Errorf("failed to get hosts from inventory: %w", err)
	}
	for _, host := range inventoryHosts {
		defs = append(defs, models.EventDefinition{
			Title:                   fmt.Sprintf("Missing logs for %s - System", host.hostname),
			Description:             fmt.Sprintf("We didn't receive any system logs during the day for %s", host.hostname),
			Query:                   fmt.Sprintf("source:%s AND NOT (_exists_:container_id OR _exists_:filebeat_container_id)", host.hostname),
			ExecuteEvery:            6 * time.Hour,
			NotificationGracePeriod: 12 * time.Hour,
			SearchWithin:            24 * time.Hour,
			EventOnRecordsFound:     true,
		})

		if host.docker {
			defs = append(defs, models.EventDefinition{
				Title:                   fmt.Sprintf("Missing logs for %s - Docker", host.hostname),
				Description:             fmt.Sprintf("We didn't receive any Docker logs during the day for %s", host.hostname),
				Query:                   fmt.Sprintf("source:%s AND (_exists_:container_id OR _exists_:filebeat_container_id)", host.hostname),
				ExecuteEvery:            6 * time.Hour,
				NotificationGracePeriod: 12 * time.Hour,
				SearchWithin:            24 * time.Hour,
				EventOnRecordsFound:     true,
			})
		}
	}
	return defs, nil
}

func main() {
	// Read password
	username := "admin"
	fmt.Printf(`Graylog password for "%s": `, username)
	passwordBytes, err := term.ReadPassword(int(syscall.Stdin))
	if err != nil {
		log.Fatal("Failed to read password", err)
	}
	password := string(bytes.TrimSpace(passwordBytes))

	// Create API client
	client, err := api.NewClient("https://logs.jensw.eu/api/", username, password)
	if err != nil {
		log.Fatal("Failed to create API client", err)
	}

	// Fetch event definitions
	actualDefs, err := client.ListEventDefinitions()
	if err != nil {
		log.Fatal("Failed to list event definitions", err)
	}

	// Compare event definitions
	expectedDefs, err := expectedEventDefinitions("../../inventory.yml")
	if err != nil {
		log.Fatal("Failed to get expected definitions", err)
	}
	toAdd, toUpdate, toDelete := diffEventDefinitionsByName(actualDefs, expectedDefs)

	// Add event definitions
	if len(toAdd) > 0 {
		fmt.Println("Creating event definitions:")
	}
	for _, ed := range toAdd {
		fmt.Println("-", ed.Title)
		_, err := client.CreateEventDefinition(ed)
		if err != nil {
			log.Fatal("Failed to create event definition", err)
		}
	}

	// Update event definitions
	if len(toUpdate) > 0 {
		fmt.Println("Updating event definitions:")
	}
	for _, ed := range toUpdate {
		fmt.Println("-", ed.Title)
		_, err := client.UpdateEventDefinition(ed.ID, ed)
		if err != nil {
			log.Fatal("Failed to update event definition", err)
		}
	}

	// Delete event definitions
	if len(toDelete) > 0 {
		fmt.Println("Deleting event definitions:")
	}
	for _, ed := range toDelete {
		fmt.Println("-", ed.Title)
		err := client.DeleteEventDefinition(ed.ID)
		if err != nil {
			log.Fatal("Failed to delete event definition", err)
		}
	}
}

func diffEventDefinitionsByName(actual, expected []models.EventDefinition) (toAdd, toUpdate, toDelete []models.EventDefinition) {
	// Init
	toAdd = []models.EventDefinition{}
	toUpdate = []models.EventDefinition{}
	actualMap := make(map[string]models.EventDefinition, len(actual))
	for _, a := range actual {
		actualMap[a.Title] = a
	}

	// Check for defs to add/update
	for _, e := range expected {
		actualDef, exists := actualMap[e.Title]
		if exists {
			e.ID = actualDef.ID
			toUpdate = append(toUpdate, e)
			delete(actualMap, e.Title)
		} else {
			toAdd = append(toAdd, e)
		}
	}

	// Check for defs to delete
	toDelete = make([]models.EventDefinition, 0, len(actualMap))
	for _, a := range actualMap {
		toDelete = append(toDelete, a)
	}
	return
}

type InventoryHost struct {
	hostname string
	docker   bool
}

func getHostsFromInventory(path string) ([]InventoryHost, error) {
	// Fetch inventory
	cmd := exec.Command("ansible-inventory", "--export", "--list", "--limit", "!ungrouped", "--inventory", path)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, fmt.Errorf("failed to get inventory content using ansible-inventory: %w", err)
	}

	// Parse inventory
	var groups map[string]InventoryGroup
	err = json.Unmarshal(output, &groups)
	if err != nil {
		return nil, fmt.Errorf("failed to parse inventory output: %w", err)
	}

	// Convert inventory to hosts
	return inventoryGroupsToHosts(groups), nil
}

type InventoryGroup struct {
	Children []string `json:"children"`
	Hosts    []string `json:"hosts"`
	HostVars any      `json:"hostvars"`
}

func inventoryGroupsToHosts(groups map[string]InventoryGroup) []InventoryHost {
	all, _ := getHostsForGroup(groups, "all")
	docker, _ := getHostsForGroup(groups, "docker_host")

	result := make([]InventoryHost, len(all))
	for i, h := range all {
		result[i] = InventoryHost{
			hostname: h,
			docker:   slices.Contains(docker, h),
		}
	}
	slices.SortFunc(result, func(a, b InventoryHost) int {
		return strings.Compare(a.hostname, b.hostname)
	})
	return result
}

func getHostsForGroup(groups map[string]InventoryGroup, child string) (hosts, children []string) {
	// Ignore group "ungrouped"
	if child == "ungrouped" {
		return nil, nil
	}

	// Get nested hosts/groups
	hosts = groups[child].Hosts
	for _, subChild := range groups[child].Children {
		subHosts, _ := getHostsForGroup(groups, subChild)
		hosts = append(hosts, subHosts...)
	}

	// Make hosts unique
	slices.Sort(hosts)
	hosts = slices.Compact(hosts)
	return hosts, nil
}
