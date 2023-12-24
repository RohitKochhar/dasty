# Imports ---------------------------------------------------------------------
# Standard library imports
import requests # type: ignore
# Local application imports
from .utils import check_response_body_contains, replace_variables, check_response_length

# Classes ---------------------------------------------------------------------
class Step:
    def __init__(
            # Required parameters
            self,
            name: str,
            method: str,
            url: str,
            expected_status_code: int,
            # Optional parameters
            headers: dict = None,
            response_includes: dict = None, 
            response_excludes: dict = None,
            response_length: dict = None,
            request_body: dict = None, 
            extract: list = None,
            output: list = None,
            expect: dict = None,
        ) -> None:
        """
        Constructs a Step object from the given parameters.
        """
        # Required parameters
        self.name = name
        self.method = method
        self.url = url
        self.expected_status_code = expected_status_code
        # Optional parameters
        self.headers = headers
        self.request_body = request_body
        self.response_includes = response_includes
        self.response_excludes = response_excludes
        self.response_length = response_length
        self.extract = extract
        self.output = output
        self.expect = expect

    def __call__(self, variables) -> dict:
        print(f"\tRunning step {self.name}...", end="")
        # Replace variables in the url
        self.url = self.url.format(**variables).replace("$", "")
        self.request_body = {key: value.format(**variables).replace("$", "") for key, value in self.request_body.items()} if self.request_body is not None else None
  
        method_func = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
            "PATCH": requests.patch,
            "HEAD": requests.head,
            "OPTIONS": requests.options,
        }.get(self.method)

        if not method_func:
            raise ValueError(f"Unsupported HTTP method: {self.method}")

        # Call the requests function with the provided parameters
        if self.method in ["GET", "HEAD", "OPTIONS"]:
            response = method_func(self.url, headers=self.headers)
        elif self.method in ["POST", "PUT", "PATCH", "DELETE"]:
            response = method_func(self.url, json=self.request_body, headers=self.headers)
        else:
            # NOTE: This block is unreachable, but is kept here for completeness
            raise ValueError(f"Unsupported HTTP method: {self.method}")

        assert response.status_code == self.expected_status_code, f'Error during \"{self.name}\" step:\nExpected {self.expected_status_code}, instead got {response.status_code}'
        
        # Replace variables in response_includes and perform the check
        if self.response_includes is not None:
            formatted_response_includes = replace_variables(self.response_includes, variables)
            response_json = response.json()
            assert check_response_body_contains(response_json, formatted_response_includes), f'Error during \"{self.name}\" step:\nResponse: \n{response_json}\n Does not contain: \n{formatted_response_includes}'

        # Replace variables in response_excludes and perform the check
        if self.response_excludes is not None:
            formatted_response_excludes = replace_variables(self.response_excludes, variables)
            response_json = response.json()
            assert not check_response_body_contains(response_json, formatted_response_excludes), f'Error during \"{self.name}\" step:\nResponse: \n{response_json}\n Contains: \n{formatted_response_excludes}'

        # Replace variables in response_length and perform the check
        if self.response_length is not None:
            formatted_response_length = replace_variables(self.response_length, variables)
            response_json = response.json()
            assert check_response_length(response_json, formatted_response_length), f'Error during "{self.name}" step:\nResponse length mismatch in: \n{response_json}\nExpected lengths: \n{formatted_response_length}'

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

        # Print variables if specified
        if self.output:
            print("\t\tOutputs:")
            for println in self.output:
                formatted_println = replace_variables(println, variables)
                print(f"\t\t- {formatted_println}")

        if self.expect:
            for expectation in self.expect:
                variable_name = expectation['variable']
                variable = replace_variables(variable_name, variables)
                if variable_name == variable:
                    raise ValueError(f"Variable {variable_name} not found in variables")
                operator = expectation['operator']
                value = replace_variables(expectation['value'], variables)
                if operator == 'eq':
                    assert str(variable) == str(value), f'Error during \"{self.name}\" step:\nExpected {variable_name} to be equal to {value}, instead got {variable}'
                if operator == 'ne':
                    assert str(variable) != str(value), f'Error during \"{self.name}\" step:\nExpected {variable_name} to be not equal to {value}, instead got {variable}'

        return variables
