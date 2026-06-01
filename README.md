# Project 2 - Server Health Checker

<aside>

💡 About the project**:**

**Server Health Checker** is a Python script that automatically checks whether a list of servers and services are up and responding correctly. Instead of manually opening each URL or waiting for users to report outages, you run one script and instantly know the status of everything.

The script takes a list of service endpoints and sends an HTTP request to each one. For every endpoint it checks three things: did it respond with a success status code, how long did it take to respond, and does the JSON body contain `"status": "ok"`. Based on those three checks it decides whether the service is healthy or not.

If a service responds but takes longer than 500ms, it prints a warning even if the service is technically up. If a service is completely down or returns an error code, it gets saved to a separate list of failed services so you have a record of what needs attention.

To make development and testing easy, you can use:

Bin -API as the **default test environment for simulating real services**

During development, users should test using these endpoints:

- `https://httpbin.org/status/200` → healthy service
- `https://httpbin.org/status/500` → failing service
- `https://httpbin.org/delay/2` → slow service
- `https://httpbin.org/json` → valid JSON response

Build it as small features, not one big problem.

</aside>

### Feature-1: Load the list of servers

**Goal:** Get a list of URLs from outside your code.

**Support at least one of these:**

Option A — Environment variable:

```bash
SERVERS="https://httpbin.org/status/200,https://httpbin.org/status/500"
```

Option B — Config file:

```json
{
  "servers": [
    "https://httpbin.org/status/200",
    "https://httpbin.org/json"
  ]
}
```

**Expected result:**

```
Loaded 3 servers
```

### Feature-2: Send a request to one server

**Goal:** Write a function that checks a single URL and returns the result.

**What it must do:**

- Send an HTTP GET request to the URL
- Get the response
- Return the status code and URL as a result**Expected result:**

```json
{
  "url": "https://httpbin.org/status/200",
  "status_code": 200
}
```

### Feature-3: Measure response time

**Goal:** Know how fast each server responds.

**What to do:**

- Start a timer before sending the request
- Stop the timer after receiving the response
- Calculate the elapsed time in milliseconds

**Expected result:**

```
120ms
```

### Feature-4: Check if a server is healthy

**Goal:** Decide whether a service is up or down based on the response.

**Rules:**

Healthy if:

- Status code is 200–299
- Request completes without error
Unhealthy if:
- Status code is 400 or above
- Request times out or fails entirely

**Test endpoints:**

```
https://httpbin.org/status/200   → healthy
https://httpbin.org/status/500   → failing
```

### Feature-5: Validate JSON body

**Goal:** If the response is JSON, check its content to confirm the service is truly healthy.

**Rule:** If the response contains `{ "status": "ok" }`, mark the service as OK.

**Test endpoint:**

```
https://httpbin.org/json
```

### Feature-6: Detect slow services

**Goal:** Warn if a service responds but takes too long.

**Rule:** If response time is over 500ms, flag it as slow.

**Test endpoint:**

```
https://httpbin.org/delay/2
```

**Expected output:**

```
slow response — 2100ms
```

### Feature-7: Print results per service

**Goal:** Display a clear, consistent status line for every server checked.

**Expected output:**

```
api.service.com    — OK (200)    — 120ms
db.service.com    — OK (200)    — 620ms  [slow]
auth.service.com  — DOWN (500)
cache.service.com — TIMEOUT
```

### Feature-8: Save failed services

**Goal:** Keep a record of every service that failed so you can report them at the end.

**What to do:**

- Create a list: `failed_services = []`
- Append to it on timeout, 500 errors, or any request failure

**Expected result:**

```
Failed services: auth.service.com, cache.service.com
```

### Feature-9: Flexible config loading

**Goal:** Make the script work regardless of whether config comes from an env variable or a file.

**Rule:**

- Check for the env variable first
- Fall back to the config file if the env variable is not set
- Raise a clear error if neither is found

### Feature-10: Organize code into functions

**Goal:** Make the code readable, reusable, and easy to extend.

**Required functions:**

- `load_servers()` — reads config and returns list of URLs
- `check_server(url)` — checks a single URL and returns its result
- `check_all_servers()` — runs checks across all servers
- `format_result(result)` — formats a single result into a readable string

### Feature-11: Run checks in parallel

Use `threading` or `concurrent.futures` to check all servers at the same time instead of one by one. A slow server won't hold up the rest.

### Feature-12: Retry failed requests

Before marking a service as down, retry the request 1–2 times. Only mark it as failed if all attempts fail.

### Feature-13: Send alerts

When a service fails, send a notification via email so the right person knows immediately.

### Final output — what the tool should print

```
api.service.com    — OK (200)    — 120ms
db.service.com    — OK (200)    — 620ms  [slow]
auth.service.com  — DOWN (500)
cache.service.com — TIMEOUT

Failed services: auth.service.com, cache.service.com
```