# Imports ---------------------------------------------------------------------
import requests # type: ignore
import yaml # type: ignore
import re
import json

# Helper functions -----------------------------------------------------------
def check_key_value_in_json(json_data, key, value):
    str = json.dumps(json_data)
    substr = f'"{key}": {value}'
    return substr in str

def replace_variables_in_string(content, variables):
    for var, value in variables.items():
        content = re.sub(rf'\$\{{{var}\}}', value, content)
    return content

def replace_variables(content, variables):
    if isinstance(content, dict):
        return {k: replace_variables(v, variables) for k, v in content.items()}
    elif isinstance(content, list):
        return [replace_variables(item, variables) for item in content]
    elif isinstance(content, str):
        return replace_variables_in_string(content, variables)
    else:
        return content

# Classes ---------------------------------------------------------------------
class YAMLScenario:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        with open(filepath, 'r') as f:
            yaml_content = yaml.safe_load(f)
        
        variables = yaml_content.get('variables', {})
        yaml_content = replace_variables(yaml_content, variables)
        self.name = yaml_content['name']
        self.description = yaml_content['description']
        self.steps = [Step(**step) for step in yaml_content['steps']]


    def run(self) -> None:
        print(f"Running scenario {self.name} defined in {self.filepath}...")
        for step in self.steps:
            step()
        print("\033[92m" + f"{self.name} Success ✅" + "\033[0m")      


class Step:
    def __init__(self, name: str, method: str, url: str, expected_status_code: int, response_contains: dict = None, request_body: dict = None) -> None:
        self.name = name
        self.method = method
        self.url = url
        self.expected_status_code = expected_status_code
        self.request_body = request_body
        self.response_contains = response_contains

    def __call__(self) -> None:
        print(f"\tRunning step {self.name}...", end="")
        if self.method == "GET":
            response = requests.get(self.url)
        elif self.method == "POST":
            response = requests.post(self.url, json=self.request_body)
        elif self.method == "DELETE":
            response = requests.delete(self.url)
        else:
            raise ValueError(f"Invalid method {self.method}")
        assert response.status_code == self.expected_status_code, f'Error during \"{self.name}\" step:\nExpected {self.expected_status_code}, instead got {response.status_code}'
        
        # Check if the response contains the expected key-value pair (simple structure)
        if self.response_contains is not None:
            response_json = response.json()
            for key, value in self.response_contains.items():
                assert check_key_value_in_json(response_json, key, value), f"Response JSON does not contain the expected {key}: {value}\n{response_json}"
        
        print("\033[92m" + f" Success ✅" + "\033[0m")
