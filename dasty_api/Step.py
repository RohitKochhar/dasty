# Imports ---------------------------------------------------------------------
# Standard library imports
import requests # type: ignore
# Local application imports
from .utils import check_response_body_contains

# Classes ---------------------------------------------------------------------
class Step:
    def __init__(self, name: str, method: str, url: str, expected_status_code: int, response_contains: dict = None, request_body: dict = None, save_response_values: list = None) -> None:
        self.name = name
        self.method = method
        self.url = url
        self.expected_status_code = expected_status_code
        self.request_body = request_body
        self.response_contains = response_contains
        self.save_response_values = save_response_values

    def __call__(self, variables) -> dict:
        print(f"\tRunning step {self.name}...", end="")
        # Replace variables in the url
        self.url = self.url.format(**variables).replace("$", "")

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
            assert check_response_body_contains(response_json, self.response_contains), f'Error during \"{self.name}\" step:\Response: \n{response_json}\n Does not contain: \n{self.response_contains}'

        # Save response values into variables if specified
        if self.save_response_values:
            response_json = response.json()
            for item in self.save_response_values:
                variable_name = item['name']
                path = item['from'].split('.')
                value = response_json
                for p in path:
                    value = value.get(p)
                variables[variable_name] = value

        print("\033[92m" + f" Success ✅" + "\033[0m")

        return variables
