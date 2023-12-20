# Dasty: Declarative API Scenario Testing in YAML

Dasty is a Python package designed to simplify the process of testing APIs by allowing tests to be defined declaratively in YAML format. This approach enables easy-to-write, easy-to-read API test scenarios, making API testing more accessible and maintainable.

## Features

- **Declarative Syntax**: Define API tests in a simple, human-readable YAML format.
- **Flexible Test Scenarios**: Support various HTTP methods and validations.
- **Easy Variable Substitution**: Define and use variables within your YAML test scenarios.

## Installation

To install Dasty, simply use pip:

```bash
pip install dasty_api
```

## Usage

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

The recommended structure is creating a folder named `dasty_tests`, containing a sub-folder named `scenarios`, along with a `main.py` file which looks like:

```python
from dasty_api.dasty import YAMLScenario
import pathlib
import sys

if __name__ == "__main__":
    # Use the provided file path if one is provided
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        scenario = YAMLScenario(filepath=filepath)
        scenario.run()
    # Otherwise, run all the scenarios in the scenarios directory
    else:
        scenario_directory = pathlib.Path("./scenarios")
        # Get each file name in the target directory
        scenario_filepaths = [str(path) for path in scenario_directory.glob("*.yaml")]
        # Create a YAML scenario for each file
        scenarios = [YAMLScenario(filepath=filepath) for filepath in scenario_filepaths]
        for scenario in scenarios:
            scenario.run()
```

Then, the `dasty-tests` folder should look like:
```
.
├── main.py
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
