# Imports ---------------------------------------------------------------------
# Standard library imports
import requests # type: ignore
# Local application imports
from .utils import check_response_body_contains, replace_variables

# Classes ---------------------------------------------------------------------
class Step:
    def __init__(
            self,
            name: str,
            method: str,
            url: str,
            expected_status_code: int,
            response_includes: dict = None, 
            response_excludes: dict = None,
            request_body: dict = None, 
            extract: list = None
        ) -> None:
        """
        Constructs a Step object from the given parameters.
        """
        self.name = name
        self.method = method
        self.url = url
        self.expected_status_code = expected_status_code
        self.request_body = request_body
        self.response_includes = response_includes
        self.response_excludes = response_excludes
        self.extract = extract

    def __call__(self, variables) -> dict:
        print(f"\tRunning step {self.name}...", end="")
        # Replace variables in the url
        self.url = self.url.format(**variables).replace("$", "")
        self.request_body = {key: value.format(**variables).replace("$", "") for key, value in self.request_body.items()} if self.request_body is not None else None
  
        if self.method == "GET":
            response = requests.get(self.url)
        elif self.method == "POST":
            response = requests.post(self.url, json=self.request_body)
        elif self.method == "DELETE":
            response = requests.delete(self.url)
        else:
            raise ValueError(f"Invalid method {self.method}")
        assert response.status_code == self.expected_status_code, f'Error during \"{self.name}\" step:\nExpected {self.expected_status_code}, instead got {response.status_code}'
        
        # Replace variables in response_includes and perform the check
        if self.response_includes is not None:
            formatted_response_includes = replace_variables(self.response_includes, variables)
            response_json = response.json()
            assert check_response_body_contains(response_json, formatted_response_includes), f'Error during \"{self.name}\" step:\nResponse: \n{response_json}\n Does not contain: \n{formatted_response_includes}'

        if self.response_excludes is not None:
            formatted_response_excludes = replace_variables(self.response_excludes, variables)
            response_json = response.json()
            assert not check_response_body_contains(response_json, formatted_response_excludes), f'Error during \"{self.name}\" step:\nResponse: \n{response_json}\n Contains: \n{formatted_response_excludes}'

        # Save response values into variables if specified
        if self.extract:
            response_json = response.json()
            for item in self.extract:
                variable_name = item['name']
                path = item['from'].split('.')
                value = response_json
                for p in path:
                    value = value.get(p)
                variables[variable_name] = value

        print("\033[92m" + f" Success ✅" + "\033[0m")

        return variables
