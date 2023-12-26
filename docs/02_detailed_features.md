# Detailed Features of Dasty

Dasty is a versatile tool for API testing and benchmarking, offering a range of features to facilitate easy and efficient API scenario testing. This document provides an in-depth look at each of Dasty's features along with practical examples.

## 1. Declarative API Testing

Dasty allows you to define API tests declaratively in YAML format. This approach simplifies writing and maintaining API tests.

### Example:

```yaml
- name: "Get User Information"
  method: "GET"
  url: "http://example.com/api/user/123"
  expected_status_code: 200
  response_includes:
    username: "john_doe"
    email: "john@example.com"
```

### Benefits:

- **Readability**: Easy to read and write, even for those not familiar with programming.
- **Maintainability**: Simplifies updates and modifications to tests.

## 2. Benchmarking

The Benchmarking feature provides performance metrics for each API call in your scenarios, including response time and payload sizes. You can specify the output format (`json`, `yaml`, `csv`, or `table`) to tailor the presentation of these metrics.

### Example Usage:

```python
from dasty import Benchmarker

# Specifying the output format as an optional parameter. Default is 'table'.
benchmarker = Benchmarker(directory="path/to/your/scenarios", output="json")
benchmarker.run()
```

### Output Formats:

- `table` (default): Displays the data in a table format.
- `csv`: Outputs the data in CSV format.
- `json`: Formats the data as a JSON object.
- `yaml`: Presents the data in YAML format.

### Output Metrics:

- **Time (ms)**: Execution time of each request.
- **Request Size (bytes)**: Size of the request payload.
- **Response Size (bytes)**: Size of the response payload.

### Sample Outputs:

**Table Output:**

```
Sample Service: Health Checks
-----------------------------
method    url                              time_ms    request_size    response_size
--------  -----------------------------  ---------  --------------  ---------------
GET       http://127.0.0.1:2396/healthz       1.51               0                2
GET       http://127.0.0.1:2396/readyz        1.58               0                2
```

**CSV Output:**

```
Scenario,"Add, Get, and Delete Users"
method,url,time_ms,request_size,response_size
GET,http://127.0.0.1:2396/,2.23,0,2
GET,http://127.0.0.1:2396/users,1.58,0,84
...
```

**JSON Output:**

```json
{
    "scenario_name": "Add, Get, and Delete Users",
    "stats": [
        {
            "method": "GET",
            "url": "http://127.0.0.1:2396/",
            "time_ms": "2.17",
            "request_size": 0,
            "response_size": 2
        },
        ...
    ]
}
```

**YAML Output:**

```yaml
scenario_name: Add, Get, and Delete Users
stats:
- method: GET
  url: http://127.0.0.1:2396/
  time_ms: '2.08'
  request_size: 0
  response_size: 2
- method: GET
  ...
```

## 3. Flexible Test Scenarios

Dasty supports various HTTP methods and validations, making it suitable for testing a wide range of APIs.

### Example:

```yaml
- name: "Create New User"
  method: "POST"
  url: "http://example.com/api/users"
  request_body:
    username: "new_user"
    password: "password123"
  expected_status_code: 201

- name: "Delete User"
  method: "DELETE"
  url: "http://example.com/api/users/new_user"
  expected_status_code: 200
```

## 4. Variable Substitution and Dynamic Passing

Variables can be defined and dynamically passed between test steps, enhancing the flexibility of your tests.

### Example:

```yaml
variables:
  base_url: "http://example.com/api"

steps:
  - name: "Login"
    method: "POST"
    url: "${base_url}/login"
    request_body:
      username: "user"
      password: "pass"
    extract:
      - name: auth_token
        from: token

  - name: "Fetch User Data"
    method: "GET"
    url: "${base_url}/user/data"
    headers:
      Authorization: "Bearer ${auth_token}"
    expected_status_code: 200
```

## 5. Response Validation Functions

Dasty includes functions to validate API response content, such as `response_includes`, `response_excludes`, and `response_length`.

### Example:

```yaml
- name: "Check User List"
  method: "GET"
  url: "http://example.com/api/users"
  expected_status_code: 200
  response_includes:
    - username: "john_doe"
  response_excludes:
    - username: "deleted_user"
  response_length:
    users: 5
```

## 6. Tag-Based Scenario Execution

Organize and run scenarios based on tags, allowing targeted testing of specific areas.

### Example:

```yaml
name: "User Operations"
tags:
  - "user_management"
steps:
  # Steps for user management
```

### Running Scenarios Based on Tags:

```python
from dasty import ScenarioRunner

runner = ScenarioRunner(directory="path/to/scenarios", tags=["user_management"])
runner.run()
```
