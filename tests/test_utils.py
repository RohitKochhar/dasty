# Imports ---------------------------------------------------------------------
# Standard library imports
import unittest
# Local application imports
from dasty_api.utils import check_response_body_contains

# Tests -----------------------------------------------------------------------
class TestUtils(unittest.TestCase):
    def test_check_response_body_contains(self):
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


if __name__ == '__main__':
    unittest.main()
