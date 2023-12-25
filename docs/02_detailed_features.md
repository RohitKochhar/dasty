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

The benchmarking feature provides performance metrics for each API call in your scenarios, including response time and payload sizes.

### Example Usage:

```python
from dasty import Benchmarker

benchmarker = Benchmarker(directory="path/to/your/scenarios")
benchmarker.run()
```

### Output Metrics:

- **Time (ms)**: Execution time of each request.
- **Request Size (bytes)**: Size of the request payload.
- **Response Size (bytes)**: Size of the response payload.

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
