package models

import "time"

type EventDefinition struct {
	ID          string
	Title       string
	Description string

	EventOnRecordsFound     bool
	ExecuteEvery            time.Duration
	MappedFields            map[string]string
	NotificationGracePeriod time.Duration
	Query                   string
	SearchWithin            time.Duration
}
