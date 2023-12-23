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

3. Run the ScenarioRunner

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
