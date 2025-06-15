package main

import (
	"testing"

	"github.com/jenswbe/setup/server/graylog-iac/models"
	"github.com/stretchr/testify/assert"
)

func TestDiffEventDefinitionsByName(t *testing.T) {
	actual := []models.EventDefinition{
		{
			Title: "to update",
		},
		{
			Title: "to delete",
		},
	}
	expected := []models.EventDefinition{
		{
			Title: "to add",
		},
		{
			Title: "to update",
		},
	}

	toAdd, toUpdate, toDelete := diffEventDefinitionsByName(actual, expected)
	assert.ElementsMatch(t, toAdd, []models.EventDefinition{{Title: "to add"}})
	assert.ElementsMatch(t, toUpdate, []models.EventDefinition{{Title: "to update"}})
	assert.ElementsMatch(t, toDelete, []models.EventDefinition{{Title: "to delete"}})
}

func TestInventoryGroupsToHosts(t *testing.T) {
	input := map[string]InventoryGroup{
		"all": {
			Children: []string{
				"ungrouped",
				"homelab",
				"vps",
				"docker_host",
			},
		},
		"docker_host": {
			Children: []string{
				"homelab_docker_host",
				"vps_docker_host",
			},
		},
		"homelab": {
			Children: []string{
				"vm_host",
				"homelab_docker_host",
			},
		},
		"homelab_docker_host": {
			Hosts: []string{
				"homelab_docker_host_1",
				"homelab_docker_host_2",
			},
		},
		"vm_host": {
			Hosts: []string{
				"vm_host_1",
				"vm_host_2",
			},
		},
		"vps": {
			Children: []string{
				"vps_docker_host",
			},
		},
		"vps_docker_host": {
			Hosts: []string{
				"vps_docker_host_1",
				"vps_docker_host_2",
			},
		},
	}
	expected := []InventoryHost{
		{
			hostname: "homelab_docker_host_1",
			docker:   true,
		},
		{
			hostname: "homelab_docker_host_2",
			docker:   true,
		},
		{
			hostname: "vm_host_1",
			docker:   false,
		},
		{
			hostname: "vm_host_2",
			docker:   false,
		},
		{
			hostname: "vps_docker_host_1",
			docker:   true,
		},
		{
			hostname: "vps_docker_host_2",
			docker:   true,
		},
	}

	actual := inventoryGroupsToHosts(input)
	assert.Equal(t, expected, actual)
}
