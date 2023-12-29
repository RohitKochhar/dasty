import unittest
from unittest.mock import patch
import dasty_api.utils as utils

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
                    self.assertEqual(utils.check_response_body_contains(test_case['json_data'], test_case['yaml_data']), test_case['expected'])
                    print("\033[92m" + " Success ✅" + "\033[0m")
                except AssertionError as e:
                    print("\033[91m" + " Failed ❌" + "\033[0m")

    def test_response_body_includes_with_list_yaml_data(self):
        test_cases = [
            {
                'name': 'List in YAML data',
                'json_data': [{'name': 'Alice'}, {'name': 'Bob'}],
                'yaml_data': [{'name': 'Alice'}, {'name': 'Bob'}],
                'expected': True
            },
            {
                'name': 'Partial match in list YAML data',
                'json_data': [{'name': 'Alice'}, {'name': 'Bob'}],
                'yaml_data': [{'name': 'Charlie'}],
                'expected': False
            },
        ]
        for test_case in test_cases:
            with self.subTest(test_case['name']):
                self.assertEqual(
                    utils.check_response_body_contains(test_case['json_data'], test_case['yaml_data']),
                    test_case['expected']
                )

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
                    result = utils.replace_variables(test_case['content'], test_case['variables'])
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
                    result = utils.replace_variables(test_case['content'], test_case['variables'])
                    self.assertEqual(result, test_case['expected'])
                    print("\033[92m" + " Success ✅" + "\033[0m")
                except AssertionError as e:
                    print("\033[91m" + " Failed ❌" + "\033[0m")

class TestCheckResponseLength(unittest.TestCase):
    def test_check_response_length(self):
        test_cases = [
            {
                'name': 'Length matches specification',
                'json_data': {'name': 'John', 'age': '30'},
                'length_spec': {'name': 4, 'age': 2},
                'expected': True,
                'expected_exception': None
            },
            {
                'name': 'Length does not match specification',
                'json_data': {'name': 'John', 'age': '30'},
                'length_spec': {'name': 5, 'age': 2},
                'expected': False,
                'expected_exception': AssertionError
            },
            {
                'name': 'Field missing in json data',
                'json_data': {'name': 'John'},
                'length_spec': {'name': 4, 'age': 2},
                'expected': None,
                'expected_exception': ValueError
            }
        ]

        print("Testing check_response_length...")
        for test_case in test_cases:
            print(f"\t{test_case['name']}...", end="")
            with self.subTest(test_case['name']):
                if test_case['expected_exception']:
                    with self.assertRaises(test_case['expected_exception']):
                        utils.check_response_length(test_case['json_data'], test_case['length_spec'])
                        print("\033[91m" + " Failed ❌" + "\033[0m")
                    print("\033[92m" + " Success ✅" + "\033[0m")
                else:
                    try:
                        self.assertEqual(
                            utils.check_response_length(test_case['json_data'], test_case['length_spec']),
                            test_case['expected']
                        )
                        print("\033[92m" + " Success ✅" + "\033[0m")
                    except AssertionError as e:
                        print("\033[91m" + " Failed ❌" + "\033[0m")

    def test_check_response_length_with_single_integer(self):
        test_cases = [
            {
                'name': 'Length matches single integer',
                'json_data': [1, 2, 3, 4],
                'length_spec': 4,
                'expected': True,
                'expected_exception': None
            },
            {
                'name': 'Length does not match single integer',
                'json_data': [1, 2, 3],
                'length_spec': 4,
                'expected': False,
                'expected_exception': AssertionError
            },
            {
                'name': 'Non-list data with single integer length',
                'json_data': {'name': 'John'},
                'length_spec': 4,
                'expected': False,
                'expected_exception': AssertionError
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case['name']):
                if test_case['expected_exception']:
                    with self.assertRaises(test_case['expected_exception']):
                        utils.check_response_length(test_case['json_data'], test_case['length_spec'])
                else:
                    self.assertEqual(
                        utils.check_response_length(test_case['json_data'], test_case['length_spec']),
                        test_case['expected']
                    )

class TestMeasureTime(unittest.TestCase):
    def test_measure_time(self):
        print("Testing measure_time...")
        with patch('dasty_api.utils.get_current_time') as mock_time:
            mock_time.side_effect = [100, 101]

            def sample_function():
                return "sample response"

            try:
                response, time_taken = utils.measure_time(sample_function)
                self.assertEqual(response, "sample response")
                self.assertEqual(time_taken, "1000.00")
                print("\tMeasure time with controlled function... \033[92m Success ✅\033[0m")
            except AssertionError as e:
                print("\tMeasure time with controlled function... \033[91m Failed ❌\033[0m")
                print(f"Expected sample response, got {response}")
                print(f"Expected 1000.00, got {time_taken}")

if __name__ == '__main__':
    unittest.main()
