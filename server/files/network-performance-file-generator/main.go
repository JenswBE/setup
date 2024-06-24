package main

import (
	"bytes"
	"fmt"
	"log/slog"
	"net/http"
	"strconv"
)

const Port = "8080"
const SizeMBParam = "size_mb"
const DefaultSizeMB = 10

func main() {
	// Init
	payload1MB := bytes.Repeat([]byte("X"), 1024*1024)

	// Start server
	slog.Info("Starting server ...", "port", Port)
	err := http.ListenAndServe(":"+Port, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Parse size param
		sizeMB, err := parseSizeParam(r.URL.Query().Get("size_mb"), DefaultSizeMB)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			_, err := w.Write([]byte(err.Error()))
			if err != nil {
				slog.Warn("Failed to write error response", "error", err)
			}
		}

		// Write response
		w.Header().Set("Content-type", "application/octet-stream")
		w.Header().Set("Content-length", fmt.Sprintf("%d", len(payload1MB)*sizeMB))
		for range sizeMB {
			_, err := w.Write(payload1MB)
			if err != nil {
				slog.Warn("Failed to write payload", "error", err)
				return
			}
		}
	}))
	slog.Error("Failed to start HTTP server", "error", err)
}

func parseSizeParam(input string, defaultValue int) (int, error) {
	if input == "" {
		return defaultValue, nil
	}

	value, err := strconv.Atoi(input)
	if err != nil {
		slog.Warn("Unable to parse value of param", "param", SizeMBParam, "value", input, "error", err)
		return 0, fmt.Errorf("unable to parse provided value for param %s as integer", SizeMBParam)
	}

	if value <= 0 {
		slog.Warn("Value of param must be a positive integer", "param", SizeMBParam, "value", input)
		return 0, fmt.Errorf("value for param %s must be a positive integer", SizeMBParam)
	}

	return value, nil
}
