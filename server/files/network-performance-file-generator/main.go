package main

import (
	"bytes"
	"flag"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os"
	"strconv"
	"time"
)

const (
	Port          = "8080"
	SizeMBParam   = "size_mb"
	DefaultSizeMB = 10
	MB            = 1024 * 1024 // 1MB
)

var Payload1MB = bytes.Repeat([]byte("X"), MB)

func main() {
	// Flags
	healthCheck := flag.Bool("healthcheck", false, "Perform a healthcheck on localhost")
	flag.Parse()

	// Perform health check
	if *healthCheck {
		if isHealthy() {
			os.Exit(0) // Success
		}
		os.Exit(1) // Error
	}

	// Run service
	if err := run(); err != nil {
		slog.Error("Starting service returned error", "error", err)
	}
}

func run() error {
	// Start server
	slog.Info("Starting server ...", "port", Port)
	server := http.Server{
		Addr:              ":" + Port,
		ReadHeaderTimeout: time.Second,
		Handler:           http.HandlerFunc(handleRequest),
	}
	err := server.ListenAndServe()
	return fmt.Errorf("failed to start HTTP server: %w", err)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
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
	w.Header().Set("Content-length", strconv.Itoa(len(Payload1MB)*sizeMB))
	for range sizeMB {
		_, err := w.Write(Payload1MB)
		if err != nil {
			slog.Warn("Failed to write payload", "error", err)
			return
		}
	}
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

func isHealthy() bool {
	checkURL := fmt.Sprintf("http://localhost:%s?%s=2", Port, SizeMBParam)
	resp, err := http.Get(checkURL) //#nosec G107 Variables are taken from constants
	if err != nil {
		slog.Warn("Healthcheck: HTTP call returned error", "error", err)
		return false
	}
	defer func() {
		if closeErr := resp.Body.Close(); closeErr != nil {
			slog.Warn("Healthcheck: Failed to close body", "error", closeErr)
		}
	}()

	if resp.ContentLength != 2*MB {
		slog.Warn("Healthcheck: HTTP call returned incorrect content length", "expected", 2048, "actual", resp.ContentLength)
		return false
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		slog.Warn("Healthcheck: Failed to read response body")
		return false
	}
	if len(body) != 2*MB {
		slog.Warn("Healthcheck: Actual response body has different length from ContentLength", "content_length", resp.ContentLength, "body_length", len(body))
		return false
	}

	slog.Info("Healthcheck successful")
	return true
}
