import unittest
from unittest.mock import patch, MagicMock
from dasty_api.Scenario import Scenario
from dasty_api.Step import Step

class TestScenario(unittest.TestCase):
    def setUp(self):
        """ Set up common attributes used in multiple tests. """
        self.filepath = 'path/to/scenario.yaml'
        self.yaml_content = {
            'name': 'Test Scenario',
            'description': 'A test scenario',
            'tags': ['test', 'example'],
            'variables': {'var1': 'value1'},
            'steps': [
                {'name': 'Step 1', 'method': 'GET', 'url': 'http://example.com', 'expected_status_code': 200}
                # ... other steps ...
            ]
        }

    @patch('builtins.open')
    @patch('yaml.safe_load')
    def test_init_success(self, mock_safe_load, mock_open):
        """ Test successful initialization of the Scenario object. """
        mock_safe_load.return_value = self.yaml_content
        scenario = Scenario(self.filepath)
        
        self.assertEqual(scenario.name, 'Test Scenario')
        self.assertEqual(scenario.description, 'A test scenario')
        self.assertEqual(scenario.tags, ['test', 'example'])
        self.assertEqual(scenario.variables, {'var1': 'value1'})
        self.assertIsInstance(scenario.steps[0], Step)

    @patch('builtins.open', new_callable=MagicMock)
    def test_init_file_empty(self, mock_open):
        """ Test initialization behavior when the YAML file is empty. """
        mock_open.return_value.__enter__.return_value.read.return_value = ""
        
        with self.assertRaises(ValueError):
            Scenario(self.filepath)

    @patch('builtins.open')
    @patch('yaml.safe_load')
    def test_run_scenario(self, mock_safe_load, mock_open):
        """ Test the execution of steps in the scenario. """
        mock_safe_load.return_value = self.yaml_content
        scenario = Scenario(self.filepath)

        with patch.object(Scenario, '_validate_scenario') as mock_validate:
            with patch.object(Step, '__call__', return_value={}) as mock_step:
                scenario.run()
                self.assertEqual(mock_step.call_count, len(self.yaml_content['steps']))

    @patch('builtins.open')
    @patch('yaml.safe_load')
    def test_validate_scenario_missing_name(self, mock_safe_load, mock_open):
        """ Test scenario validation when the 'name' attribute is missing. """
        yaml_content_missing_name = {
            'description': 'A test scenario',
            'steps': [{'name': 'Step 1', 'method': 'GET', 'url': 'http://example.com', 'expected_status_code': 200}]
        }
        mock_safe_load.return_value = yaml_content_missing_name

        with self.assertRaises(ValueError) as context:
            Scenario(self.filepath)

        self.assertIn("Scenario name is required", str(context.exception))

    @patch('builtins.open')
    @patch('yaml.safe_load')
    def test_validate_scenario_missing_steps(self, mock_safe_load, mock_open):
        """ Test scenario validation when the 'steps' attribute is missing. """
        yaml_content_missing_steps = {
            'name': 'Test Scenario',
            'description': 'A test scenario'
        }
        mock_safe_load.return_value = yaml_content_missing_steps

        with self.assertRaises(ValueError) as context:
            Scenario(self.filepath)

        self.assertIn("Scenario steps are required", str(context.exception))


if __name__ == '__main__':
    unittest.main()
