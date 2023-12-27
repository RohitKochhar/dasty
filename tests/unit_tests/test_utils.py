# Imports ---------------------------------------------------------------------
# Standard library imports
import unittest
# Local application imports
from dasty_api.utils import check_response_body_contains, replace_variables, replace_variables_in_string

# Tests -----------------------------------------------------------------------
class TestCheckResponseBodyIncludes(unittest.TestCase):
    def test_response_body_includes(self):
        test_cases = [
            {
                'name': 'Simple structure',
                'json_data': {'name': 'John', 'age': 30},
                'yaml_data': {'name': 'John'},
                'expected': True
            },
            {
                'name': 'Simple structure with multiple keys',
                'json_data': {'name': 'John', 'age': 30},
                'yaml_data': {'name': 'John', 'age': 30},
                'expected': True
            },
            {
                'name': 'Simple structure with multiple keys, one missing',
                'json_data': {'name': 'John', 'age': 30},
                'yaml_data': {'name': 'John', 'age': 30, 'country': 'USA'},
                'expected': False
            },
            {
                'name': 'Simple structure with multiple keys, one different',
                'json_data': {'name': 'John', 'age': 30},
                'yaml_data': {'name': 'John', 'age': 31},
                'expected': False
            },
            {
                'name': 'Response is an array',
                'json_data': {'fruits': ['apple', 'banana', 'cherry']},
                'yaml_data': {'fruits': ['apple', 'banana']},
                'expected': True
            },
            {
                'name': "Response contains nested objects, check for single match",
                'json_data': {'players': [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]},
                'yaml_data': {'players': [{"name": "John"}]},
                'expected': True
            },
            {
                'name': "Response contains nested objects, check for multiple matches",
                'json_data': {'players': [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]},
                'yaml_data': {'players': [{"name": "John"}, {"name": "Jane"}]},
                'expected': True
            }
        ]
        print("Testing check_response_body_contains...")
        for test_case in test_cases:
            print(f"\t{test_case['name']}...", end="")
            with self.subTest(test_case['name']):
                try:
                    self.assertEqual(check_response_body_contains(test_case['json_data'], test_case['yaml_data']), test_case['expected'])
                    print("\033[92m" + " Success ✅" + "\033[0m")
                except AssertionError as e:
                    print("\033[91m" + " Failed ❌" + "\033[0m")

class TestVariableReplacement(unittest.TestCase):
    def test_replace_variables_in_string(self):
        test_cases = [
            {
                'name': 'Simple variable replacement',
                'content': 'Hello ${name}',
                'variables': {'name': 'World'},
                'expected': 'Hello World'
            },
            {
                'name': 'Multiple variable replacements',
                'content': '${greeting}, ${name}!',
                'variables': {'greeting': 'Hello', 'name': 'World'},
                'expected': 'Hello, World!'
            },
            {
                'name': 'Variable not in dictionary',
                'content': 'Hello ${name}',
                'variables': {'other': 'World'},
                'expected': 'Hello ${name}'
            },
            {
                'name': 'Empty variables dictionary',
                'content': 'Hello ${name}',
                'variables': {},
                'expected': 'Hello ${name}'
            },
            {
                'name': 'No variables in string',
                'content': 'Hello World',
                'variables': {'name': 'Universe'},
                'expected': 'Hello World'
            }
        ]
        print("Testing replace_variables...")
        for test_case in test_cases:
            print(f"\t{test_case['name']}...", end="")
            with self.subTest(test_case['name']):
                try:
                    result = replace_variables(test_case['content'], test_case['variables'])
                    self.assertEqual(result, test_case['expected'])
                    print("\033[92m" + " Success ✅" + "\033[0m")
                except AssertionError as e:
                    print("\033[91m" + " Failed ❌" + "\033[0m")

    def test_replace_variables(self):
        test_cases = [
            {
                'name': 'Replace in dictionary',
                'content': {'message': 'Hello ${name}', 'year': '${year}'},
                'variables': {'name': 'Alice', 'year': 2021},
                'expected': {'message': 'Hello Alice', 'year': '2021'}
            },
            {
                'name': 'Replace in list',
                'content': ['${item1}', '${item2}'],
                'variables': {'item1': 'apple', 'item2': 'banana'},
                'expected': ['apple', 'banana']
            },
            {
                'name': 'Nested structures',
                'content': {'items': ['${item1}', '${item2}'], 'msg': 'Hello ${name}'},
                'variables': {'item1': 'apple', 'item2': 'banana', 'name': 'Alice'},
                'expected': {'items': ['apple', 'banana'], 'msg': 'Hello Alice'}
            },
            {
                'name': 'Content without variables',
                'content': {'message': 'Hello World', 'year': 2021},
                'variables': {'name': 'Alice', 'year': 2020},
                'expected': {'message': 'Hello World', 'year': 2021}
            }
        ]
        print("Testing replace_variables...")
        for test_case in test_cases:
            print(f"\t{test_case['name']}...", end="")
            with self.subTest(test_case['name']):
                try:
                    result = replace_variables(test_case['content'], test_case['variables'])
                    self.assertEqual(result, test_case['expected'])
                    print("\033[92m" + " Success ✅" + "\033[0m")
                except AssertionError as e:
                    print("\033[91m" + " Failed ❌" + "\033[0m")

if __name__ == '__main__':
    unittest.main()
