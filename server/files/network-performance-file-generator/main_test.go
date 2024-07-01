package main

import (
	"testing"
	"time"
)

func Test(t *testing.T) {
	go func() {
		if serviceErr := run(); serviceErr != nil {
			t.Logf("service returned error: %v", serviceErr)
		}
	}()

	time.Sleep(200 * time.Millisecond)

	if !isHealthy() {
		t.Fatal("Service is not healthy")
	}
}
