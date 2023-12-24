# Imports ---------------------------------------------------------------------
import requests # type: ignore
from .utils import check_response_body_contains, replace_variables, check_response_length

# Classes ---------------------------------------------------------------------
class Step:
    def __init__(self, name: str, method: str, url: str, expected_status_code: int,
                 headers: dict = None, response_includes: dict = None,
                 response_excludes: dict = None, response_length: dict = None,
                 request_body: dict = None, extract: list = None,
                 output: list = None, expect: dict = None) -> None:
        """
        Constructs a Step object from the given parameters.
        """
        self.name = name
        self.method = method.upper()
        self.url = url
        self.expected_status_code = expected_status_code
        self.headers = headers or {}
        self.request_body = request_body
        self.response_includes = response_includes
        self.response_excludes = response_excludes
        self.response_length = response_length
        self.extract = extract
        self.output = output
        self.expect = expect

    def __call__(self, variables) -> dict:
        print(f"\tRunning step {self.name}...", end="")
        self._prepare_request(variables)
        response = self._make_request()
        self._validate_response(response, variables)
        print("\033[92m Success ✅\033[0m")
        return variables

    def _prepare_request(self, variables):
        self.url = replace_variables(self.url, variables)
        if self.request_body:
            self.request_body = {k: replace_variables(v, variables)
                                 for k, v in self.request_body.items()}

    def _make_request(self):
        request_methods = {
            "GET": requests.get, "POST": requests.post,
            "PUT": requests.put, "DELETE": requests.delete,
            "PATCH": requests.patch, "HEAD": requests.head,
            "OPTIONS": requests.options
        }

        method_func = request_methods.get(self.method)
        if not method_func:
            raise ValueError(f"Unsupported HTTP method: {self.method}")

        if self.method in ["GET", "HEAD", "OPTIONS"]:
            return method_func(self.url, headers=self.headers)
        else:
            return method_func(self.url, json=self.request_body, headers=self.headers)

    def _validate_response(self, response, variables):
        assert response.status_code == self.expected_status_code, \
            f'Error during \"{self.name}\" step: Expected {self.expected_status_code}, got {response.status_code}'
        
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            # If the response is not JSON, wrap it in a JSON object
            response_json = {"response": response.text}
        self._check_response_contents(response_json, variables)
        self._extract_and_output(response_json, variables)
        self._verify_expectations(variables)

    def _check_response_contents(self, response_json, variables):
        if self.response_includes:
            includes = replace_variables(self.response_includes, variables)
            assert check_response_body_contains(response_json, includes), \
                f'Error during \"{self.name}\" step: Response does not include expected content.'

        if self.response_excludes:
            excludes = replace_variables(self.response_excludes, variables)
            assert not check_response_body_contains(response_json, excludes), \
                f'Error during \"{self.name}\" step: Response includes excluded content.'

        if self.response_length:
            lengths = replace_variables(self.response_length, variables)
            assert check_response_length(response_json, lengths), \
                f'Error during \"{self.name}\" step: Response length mismatch.'

    def _extract_and_output(self, response_json, variables):
        if self.extract:
            for item in self.extract:
                path = item['from'].split('.')
                value = self._get_value_from_path(response_json, path)
                variables[item['name']] = value

        if self.output:
            print("\t\tOutputs:")
            for output_line in self.output:
                formatted_output = replace_variables(output_line, variables)
                print(f"\t\t- {formatted_output}")

    def _get_value_from_path(self, data, path):
        for key in path:
            data = data.get(key)
            if data is None:
                return None
        return data

    def _verify_expectations(self, variables):
        if self.expect:
            for expectation in self.expect:
                variable = replace_variables(expectation['variable'], variables)
                operator = expectation['operator']
                value = replace_variables(expectation['value'], variables)

                if operator == 'eq':
                    assert str(variable) == str(value), \
                        f'Error during \"{self.name}\" step: {variable} is not equal to {value}.'
                elif operator == 'ne':
                    assert str(variable) != str(value), \
                        f'Error during \"{self.name}\" step: {variable} is equal to {value}.'
