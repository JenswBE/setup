package api

import (
	"errors"
	"fmt"
	"strings"

	"github.com/jenswbe/setup/server/graylog-iac/models"
)

func (c Client) ListEventDefinitions() ([]models.EventDefinition, error) {
	var resp EventDefinitionsList
	err := c.get("events/definitions", map[string]string{"per_page": "1000"}, &resp)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch event definitions: %w", err)
	}

	if resp.Total > resp.Count {
		return nil, errors.New("too many event definitions for a single page. Increase per_page param and try again")
	}

	result := make([]models.EventDefinition, 0, len(resp.EventDefinitions))
	for _, ed := range resp.EventDefinitions {
		if strings.Contains(strings.ToLower(ed.Config.Type), "system-notifications") {
			continue
		}
		result = append(result, eventDefinitionToModel(ed))
	}
	return result, nil
}

func (c Client) CreateEventDefinition(def models.EventDefinition) (models.EventDefinition, error) {
	var resp EventDefinition
	err := c.post("events/definitions", eventDefinitionFromModel(def), &resp)
	if err != nil {
		return models.EventDefinition{}, fmt.Errorf("failed to create event definition: %w", err)
	}
	return eventDefinitionToModel(resp), nil
}

func (c Client) UpdateEventDefinition(id string, def models.EventDefinition) (models.EventDefinition, error) {
	def.ID = id
	var resp EventDefinition
	err := c.put("events/definitions/"+def.ID, eventDefinitionFromModel(def), &resp)
	if err != nil {
		return models.EventDefinition{}, fmt.Errorf("failed to update event definition: %w", err)
	}
	return eventDefinitionToModel(resp), nil
}

func (c Client) DeleteEventDefinition(id string) error {
	err := c.delete("events/definitions/" + id)
	if err != nil {
		return fmt.Errorf("failed to delete event definition: %w", err)
	}
	return nil
}

type EventDefinitionsList struct {
	Total            int               `json:"total"`
	Count            int               `json:"count"`
	EventDefinitions []EventDefinition `json:"event_definitions"`
}

func eventDefinitionFromModel(m models.EventDefinition) EventDefinition {
	a := EventDefinition{
		ID:          m.ID,
		Title:       m.Title,
		Description: m.Description,

		Alert: true,
		Config: EventDefinitionConfig{
			Conditions: EventDefinitionConditions{
				Expression: nil,
			},
			EventLimit:     10,
			ExecuteEveryMs: durationToMs(m.ExecuteEvery),
			GroupBy:        []any{},
			Query:          m.Query,
			SearchWithinMs: durationToMs(m.SearchWithin),
			Series:         []EventDefinitionConfigSerie{},
			Streams:        []any{},
			Type:           "aggregation-v1",
		},
		KeySpec: []string{},
		Notifications: []EventDefinitionNotification{{
			NotificationID:         "64aee248e02dea62977adb09",
			NotificationParameters: nil,
		}},
		NotificationSettings: EventDefinitionNotificationSettings{
			GracePeriodMs: durationToMs(m.NotificationGracePeriod),
			BacklogSize:   50,
		},
		Priority: 2,
	}

	if m.EventOnRecordsFound {
		a.Config.Series = []EventDefinitionConfigSerie{{
			Field: nil,
			ID:    "count-",
			Type:  "count",
		}}
		a.Config.Conditions = EventDefinitionConditions{
			Expression: EventDefinitionConditionsExpression{
				Expr: "<",
				Left: EventDefinitionConditionsExpressionLeft{
					Expr: "number-ref",
					Ref:  "count-",
				},
				Right: EventDefinitionConditionsExpressionRight{
					Expr:  "number",
					Value: 1.0,
				},
			},
		}
	}

	if len(m.MappedFields) > 0 {
		fieldSpecs := make(map[string]EventDefinitionConfigFieldSpec, len(m.MappedFields))
		for k, v := range m.MappedFields {
			fieldSpecs[k] = EventDefinitionConfigFieldSpec{
				DataType: "string",
				Providers: []EventDefinitionConfigFieldSpecProvider{{
					Type:          "template-v1",
					Template:      "${" + v + "}",
					RequireValues: false,
				}},
			}
		}
	}

	return a
}

func eventDefinitionToModel(a EventDefinition) models.EventDefinition {
	return models.EventDefinition{
		ID:          a.ID,
		Title:       a.Title,
		Description: a.Description,

		ExecuteEvery: msToDuration(a.Config.ExecuteEveryMs),
		Query:        a.Config.Query,
		SearchWithin: msToDuration(a.Config.SearchWithinMs),
	}
}

type EventDefinition struct {
	ID          string `json:"id,omitempty"`
	Title       string `json:"title"`
	Description string `json:"description"`

	Alert                bool                                      `json:"alert"`
	Config               EventDefinitionConfig                     `json:"config"`
	KeySpec              []string                                  `json:"key_spec"`
	Priority             int                                       `json:"priority"`
	Notifications        []EventDefinitionNotification             `json:"notifications"`
	NotificationSettings EventDefinitionNotificationSettings       `json:"notification_settings"`
	FieldSpec            map[string]EventDefinitionConfigFieldSpec `json:"field_spec,omitempty"`
}

type EventDefinitionConfig struct {
	ExecuteEveryMs int                          `json:"execute_every_ms"`
	GroupBy        []any                        `json:"group_by"`
	Query          string                       `json:"query"`
	SearchWithinMs int                          `json:"search_within_ms"`
	Series         []EventDefinitionConfigSerie `json:"series"`
	Streams        []any                        `json:"streams"`
	Type           string                       `json:"type"`
	Conditions     EventDefinitionConditions    `json:"conditions"`
	EventLimit     int                          `json:"event_limit"`
}

type EventDefinitionConditions struct {
	Expression any `json:"expression"`
}

type EventDefinitionConditionsExpression struct {
	Expr  string                                   `json:"expr"`
	Left  EventDefinitionConditionsExpressionLeft  `json:"left"`
	Right EventDefinitionConditionsExpressionRight `json:"right"`
}

type EventDefinitionConditionsExpressionLeft struct {
	Expr string `json:"expr"`
	Ref  string `json:"ref"`
}
type EventDefinitionConditionsExpressionRight struct {
	Expr  string  `json:"expr"`
	Value float64 `json:"value"`
}

type EventDefinitionConfigFieldSpec struct {
	DataType  string                                   `json:"data_type"`
	Providers []EventDefinitionConfigFieldSpecProvider `json:"providers"`
}

type EventDefinitionConfigFieldSpecProvider struct {
	Type          string `json:"type"`
	Template      string `json:"template"`
	RequireValues bool   `json:"require_values"`
}

type EventDefinitionConfigSerie struct {
	Field any    `json:"field"`
	ID    string `json:"id"`
	Type  string `json:"type"`
}

type EventDefinitionNotification struct {
	NotificationID         string `json:"notification_id"`
	NotificationParameters any    `json:"notification_parameters"`
}

type EventDefinitionNotificationSettings struct {
	GracePeriodMs int `json:"grace_period_ms"`
	BacklogSize   int `json:"backlog_size"`
}
