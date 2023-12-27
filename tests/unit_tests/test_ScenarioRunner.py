import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from dasty_api.ScenarioRunner import ScenarioRunner
from dasty_api.Scenario import Scenario

class TestScenarioRunner(unittest.TestCase):
    def setUp(self):
        self.directory_name = './tests/integration_tests/test_scenarios'
        self.tags = ['tag1', 'tag2']

    @patch('pathlib.Path.exists')
    def test_init_directory_exists(self, mock_exists):
        mock_exists.return_value = True
        runner = ScenarioRunner(self.directory_name, tags=self.tags)
        self.assertEqual(runner.directory, Path(self.directory_name))
        self.assertEqual(runner.tags, self.tags)

    @patch('pathlib.Path.exists')
    def test_init_directory_not_exists(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            ScenarioRunner(self.directory_name)

    @patch('pathlib.Path.glob')
    def test_collect_scenarios(self, mock_glob):
        mock_glob.return_value = [
            Path('./tests/integration_tests/test_scenarios/healthchecks.yaml'),
            Path('./tests/integration_tests/test_scenarios/add_get_delete_users.yaml'),    
        ]
        runner = ScenarioRunner(self.directory_name)
        scenarios = runner._collect_scenarios()
        self.assertEqual(len(scenarios), 2)
        self.assertIsInstance(scenarios[0], Scenario)

    @patch.object(ScenarioRunner, '_collect_scenarios')
    @patch.object(Scenario, 'run')
    def test_run_all_scenarios(self, mock_scenario_run, mock_collect_scenarios):
        mock_collect_scenarios.return_value = [MagicMock(spec=Scenario, tags=[]), MagicMock(spec=Scenario, tags=[])]
        runner = ScenarioRunner(self.directory_name)
        runner.run()

    def test_should_run_scenario_with_ignore_tag(self):
        scenario = MagicMock(spec=Scenario)
        scenario.name = 'Test Scenario'
        scenario.tags = ['ignore']
        runner = ScenarioRunner(self.directory_name)
        self.assertFalse(runner._should_run_scenario(scenario))

    def test_should_run_scenario_with_matching_tag(self):
        scenario = MagicMock(spec=Scenario)
        scenario.name = 'Test Scenario'
        scenario.tags = ['tag1']
        runner = ScenarioRunner(self.directory_name, tags=self.tags)
        self.assertTrue(runner._should_run_scenario(scenario))

    def test_should_not_run_scenario_without_matching_tag(self):
        scenario = MagicMock(spec=Scenario)
        scenario.name = 'Test Scenario'
        scenario.tags = ['non-matching']
        runner = ScenarioRunner(self.directory_name, tags=self.tags)
        self.assertFalse(runner._should_run_scenario(scenario))

if __name__ == '__main__':
    unittest.main()
