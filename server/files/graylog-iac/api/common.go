package api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"time"
)

type Client struct {
	baseURL  *url.URL
	username string
	password string
}

func NewClient(baseURL, username, password string) (Client, error) {
	baseParsed, err := url.Parse(baseURL)
	if err != nil {
		return Client{}, fmt.Errorf("failed to parse base URL %s: %w", baseURL, err)
	}

	return Client{
		baseURL:  baseParsed,
		username: username,
		password: password,
	}, nil
}

func (c Client) newURL(apiPath string, query map[string]string) *url.URL {
	apiURL := c.baseURL.JoinPath(apiPath)
	if len(query) > 0 {
		apiQuery := apiURL.Query()
		for k, v := range query {
			apiQuery.Set(k, v)
		}
		apiURL.RawQuery = apiQuery.Encode()
	}
	return apiURL
}

func (c Client) sendRequest(method string, url string, body any, dest any) error {
	// Prepare request
	var bodyReader io.Reader
	if body != nil {
		jsonBody, err := json.Marshal(body)
		if err != nil {
			return fmt.Errorf("failed to marchal body of type %T into json: %w", body, err)
		}
		bodyReader = bytes.NewReader(jsonBody)
	}
	req, err := http.NewRequest(method, url, bodyReader)
	if err != nil {
		return fmt.Errorf("failed to build api request: %w", err)
	}
	req.SetBasicAuth(c.username, c.password)
	req.Header.Add("Accept", "application/json")
	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("X-Requested-By", "XMLHttpRequest")

	// Send request
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return fmt.Errorf("failed to send api request: %w", err)
	}
	defer resp.Body.Close()

	// Parse response
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read response body: %w", err)
	}
	if resp.StatusCode >= 400 {
		return fmt.Errorf("api returned error: %s", string(bodyBytes))
	}
	if dest != nil {
		err = json.Unmarshal(bodyBytes, dest)
		if err != nil {
			return fmt.Errorf("unable to parse json body: %w. Body: %s", err, string(bodyBytes))
		}
	}
	return nil
}

func (c Client) get(apiPath string, query map[string]string, dest any) error {
	apiURL := c.newURL(apiPath, query)
	return c.sendRequest(http.MethodGet, apiURL.String(), nil, dest)
}

func (c Client) post(apiPath string, body any, dest any) error {
	apiURL := c.newURL(apiPath, nil)
	return c.sendRequest(http.MethodPost, apiURL.String(), body, dest)
}

func (c Client) put(apiPath string, body any, dest any) error {
	apiURL := c.newURL(apiPath, nil)
	return c.sendRequest(http.MethodPut, apiURL.String(), body, dest)
}

func (c Client) delete(apiPath string) error {
	apiURL := c.newURL(apiPath, nil)
	return c.sendRequest(http.MethodDelete, apiURL.String(), nil, nil)
}

func durationToMs(d time.Duration) int {
	return int(d.Milliseconds())
}

func msToDuration(ms int) time.Duration {
	return time.Duration(ms) * time.Millisecond
}
