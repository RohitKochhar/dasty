# Dasty: Declarative API Scenario Testing in YAML

<img src="./dasty.png" alt="Dasty Logo" width="200"/>

Dasty is a Python package designed to simplify the process of testing APIs by allowing tests to be defined declaratively in YAML format. This approach enables easy-to-write, easy-to-read API test scenarios, making API testing more accessible and maintainable.

## Features

- **Declarative Syntax**: Define API tests in a simple, human-readable YAML format.
- **Flexible Test Scenarios**: Support various HTTP methods and validations.
- **Easy Variable Substitution**: Define and use variables within your YAML test scenarios.
- **Dynamic Variable Passing Between Steps**: Extract and reuse values from responses in subsequent steps.

## Installation

To install Dasty, simply use pip:

```bash
pip install dasty_api
```

## Usage

### Quickstart

This repository comes with a sample server and Scenarios that can be used for quick hands-on sandboxing.

To run these Scenarios, do the following:

0. From the `examples` sub-directory

```bash
cd ./examples
```

1. Install the dependencies required for the examples

```bash
pip install -r requirements.txt
```

2. Run the simple server. This will create a simple server that listens on `localhost:2396`

```bash
python3 simple_server.py
```

3. In a new terminal, run the ScenarioRunner

```bash
python3 scenario_runner.py
```

4. If successful, the output should look as follows:

```
Running scenario Add, Get, and Delete Users defined in examples/scenarios/add_get_delete_users.yaml...
        Running step Reset the server's memory... Success ✅
        Running step Get existing users... Success ✅
        Running step Add a new user... Success ✅
        Running step Get existing users, check that Dave was added... Success ✅
        Running step Delete a user... Success ✅
        Running step Get existing users, check that Charlie was deleted... Success ✅
        Running step Try to delete a user that doesn't exist... Success ✅
Add, Get, and Delete Users Success ✅
Running scenario Sample Service: Health Checks defined in examples/scenarios/healthchecks.yaml...
        Running step Health Check... Success ✅
        Running step Readiness Check... Success ✅
Sample Service: Health Checks Success ✅
```

### Using dasty in your project

Dasty allows you to define your API test scenarios in YAML files. Here's a basic example:

```yaml
name: "Users Service: Health Checks"
description:
  - "Health checks for the Users service"
variables:
  BASE_URL: "http://127.0.0.1:8003/api/v1/"
steps:
  - name: "Health Check"
    method: "GET"
    url: "${BASE_URL}/healthz"
    expected_status_code: 200
  - name: "Readiness Check"
    method: "GET"
    url: "${BASE_URL}/readyz"
    expected_status_code: 200
```

More examples can be found in the [`examples`](https://github.com/RohitKochhar/dasty/tree/main/examples) subdirectory.

The recommended structure is creating a folder named `dasty_tests`, containing a sub-folder named `scenarios`, containing the Scenario YAML files, along with a `scenario_runner.py` file which looks like:

```python
from dasty_api.ScenarioRunner import ScenarioRunner

if __name__ == "__main__":
    runner = ScenarioRunner("./scenarios")
    runner.run()

```

Then, the `dasty-tests` folder should look like:
```
.
├── scenario_runner.py
└── scenarios
    ├── ...
    └── sample_scenario.yaml
```

Once `main.py` is executed, the output should look as follows:

```
╰─ python3 main.py                                              
Running scenario Users Service: Health Checks defined in scenarios/healthcheck_users.yaml...
        Running step Health Check... Success ✅
        Running step Readiness Check... Success ✅
Users Service: Health Checks Success ✅
```

## Features

### Dynamic Variable Passing

Dasty supports dynamic variable passing between steps in a scenario. This allows you to extract values from the response of one step and use them in subsequent steps. For example:

```yaml
steps:
  - name: "Get user ID"
    method: "GET"
    url: "${BASE_URL}/users/name=John"
    extract:
      - name: user_id
        from: id
  - name: "Use the User ID in another request"
    method: "GET"
    url: "${BASE_URL}/users/id=${user_id}"
```

### Response Validation Functions

Dasty supports a variety of response assertion features to validate API response content.

#### `response_includes` Function

This assertion ensures specific content is included in the API response. It's essential for verifying the presence of expected data elements. For instance, to confirm that a user object is part of the response, `response_includes` can be used to assert its existence.

**Usage Example**:

```yaml
- name: "Check user presence"
  method: "GET"
  url: "${BASE_URL}/users"
  expected_status_code: 200
  response_includes:
    users:
      - name: "Alice"
```

In this example, `response_includes` will validate that within the `users` array of the response, there is an entry with the `name` attribute equal to "Alice".

A practical example of this feature can be seen in [this scenario](https://github.com/RohitKochhar/dasty/tree/main/examples/scenarios/check_response_body.yaml)

#### `response_excludes` Function

Conversely, this assertion ensures that certain content is definitively absent from the response. It is invaluable for confirming that sensitive data is not exposed or to ensure that an entity has been properly removed or is not present.

**Usage Example**:

```yaml
- name: "Validate user absence"
  method: "GET"
  url: "${BASE_URL}/users"
  expected_status_code: 200
  response_excludes:
    users:
      - name: "Alice"
```

The `response_excludes` assertion checks that the `users` array in the response does not contain any object with a `name` attribute equal to "Alice".

With these two assertions, `response_includes` and `response_excludes`, testing for both the presence and absence of data in your API responses becomes straightforward and clear, providing a robust method for validating the state and security of your API endpoints.

A practical example of this feature can be seen in [this scenario](https://github.com/RohitKochhar/dasty/tree/main/examples/scenarios/check_response_body.yaml)


### `response_length` Function

Dasty introduces the `response_length` function, enabling you to assert the length of specific fields within your API response. This is particularly useful for validating the size of arrays or strings in your response data, ensuring your API behaves as expected in terms of data quantity or size.

**Usage Example**:

To check the number of users returned by the API:

```yaml
- name: "Get existing users, check the count"
  method: "GET"
  url: "${BASE_URL}/users"
  expected_status_code: 200
  response_length:
    users: 4
```

In this example, the `response_length` check validates that the `users` field in the response contains exactly 4 items. 

This functionality is crucial for scenarios where the quantity of returned data matters, such as checking pagination results or ensuring an API does not return excessive data.

### Practical Use of `response_length`

You can combine `response_length` with other features like `response_includes` to not only validate the presence of certain data but also ensure the response contains the correct number of items.

**Combined Example**:

```yaml
- name: "Verify user list size and content"
  method: "GET"
  url: "${BASE_URL}/users"
  expected_status_code: 200
  response_includes:
    users:
      - name: "Alice"
  response_length:
    users: 4
```

In this scenario, Dasty checks that the `users` array includes a user named "Alice" and also asserts that the total number of users in the array is 4.

With `response_length`, your testing becomes more robust, allowing you to enforce not just the quality but also the quantity of the data returned by your API.


### `output` Function

Dasty also introduces an output function, enabling you to print values extracted from a response or any dynamic variable within the scenario. This feature is especially useful for debugging or when you need to log specific information.

**Usage Example**:

```yaml
steps:
  - name: "Echo Alice's ID"
    method: "POST"
    url: "${BASE_URL}/echo"
    expected_status_code: 200
    request_body:
      alice_id: "${alice_id}"
    output:
      - "Alice's ID is ${alice_id}"
```

Results in:

```
    Running step Echo Alice's ID... Success ✅
            Outputs:
            - Alice's ID is 0
```

This feature enhances the debugging capabilities within your testing scenarios, making it easier to trace and understand the flow of data.


### Variable Value Assertions

### `expect` Function

You can now perform direct comparisons of extracted variables against expected values within your scenarios. This adds an extra layer of validation to your tests, ensuring not only that your API responds correctly, but also that the content of the responses holds the expected values.

**Equality Check (`eq`)**

The `eq` operator is used to assert that a variable is equal to a specified value.

**Usage Example**:

```yaml
- name: "Check Alice's ID is 0"
  method: "GET"
  url: "${BASE_URL}/users/name=Alice"
  expected_status_code: 200
  extract:
    - name: alice_id
      from: user.id
  expect:
    - variable: ${alice_id}
      operator: eq
      value: "0"
```

In this example, the scenario validates that the ID of the user Alice is exactly `0`.

**Inequality Check (`ne`)**

Conversely, the `ne` operator is used to assert that a variable is not equal to a specified value.

**Usage Example**:

```yaml
- name: "Check Bob's ID is NOT 0"
  method: "GET"
  url: "${BASE_URL}/users/name=Bob"
  expected_status_code: 200
  extract:
    - name: bob_id
      from: user.id
  expect:
    - variable: ${bob_id}
      operator: ne
      value: "0"
```

In this example, the scenario verifies that the ID of the user Bob is not `0`.


### Tag-Based Scenario Execution

You can assign one or more tags to each scenario in your testing suite. Tags are used to categorize and selectively run scenarios based on your current testing needs.

**Defining Tags in a Scenario**:

```yaml
name: "Add, Get, and Delete Users"
description:
  - "Get the existing users, confirming that Alice, Bob, and Charlie are present"
tags:
  - "example"
```

In this example, the scenario is tagged with `"example"`. 

### Running Scenarios Based on Tags

When initializing the `ScenarioRunner`, you can specify a list of tags. The runner will then execute only those scenarios that share at least one tag with this list. This allows for targeted testing of specific parts of your application.

**Example Initialization**:

```python
ScenarioRunner(directory="...", tags=["example"])
```

Scenarios with at least one common tag with the runner's tags will be included in the test run.

### Special Tag: `ignore`

If a scenario is tagged with `ignore`, it will be excluded from all test runs, regardless of other tags it might have. This is useful for temporarily disabling certain scenarios without removing them from the suite.

**Example of Ignored Scenario**:

```yaml
name: "Temporarily Disabled Test"
tags:
  - "ignore"
```

With tag-based scenario execution, Dasty provides a more dynamic and controlled testing environment, allowing you to focus on specific areas of your application as needed.
```
