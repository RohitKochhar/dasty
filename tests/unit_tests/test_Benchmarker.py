import unittest
from unittest.mock import patch
from pathlib import Path
from dasty_api.benchmarking.Benchmarker import Benchmarker
from dasty_api.benchmarking.BenchmarkerScenario import BenchmarkerScenario

class TestBenchmarker(unittest.TestCase):
    def setUp(self):
        self.directory_name = './tests/integration_tests/test_scenarios'
        self.tags = ['performance', 'load']

    @patch('dasty_api.ScenarioRunner.__init__')
    def test_init(self, mock_scenario_runner_init):
        """ Test if Benchmarker initializes correctly """
        mock_scenario_runner_init.return_value = None
        benchmarker = Benchmarker(self.directory_name, tags=self.tags, output='table')
        self.assertEqual(benchmarker.output, 'table')

    @patch('dasty_api.ScenarioRunner.__init__')
    def test_init_with_unsupported_output(self, mock_scenario_runner_init):
        """ Test if Benchmarker defaults to 'table' output when an unsupported format is provided """
        mock_scenario_runner_init.return_value = None
        benchmarker = Benchmarker(self.directory_name, output='unsupported_format')
        self.assertEqual(benchmarker.output, 'table')

    @patch('pathlib.Path.glob')
    def test_collect_scenarios(self, mock_glob):
        """ Test if Benchmarker correctly collects scenarios """
        mock_glob.return_value = [
            Path(self.directory_name + '/healthchecks.yaml'),
            Path(self.directory_name + '/add_get_delete_users.yaml')
        ]
        benchmarker = Benchmarker(self.directory_name, output='json')
        scenarios = benchmarker._collect_scenarios()
        self.assertEqual(len(scenarios), 2)
        self.assertIsInstance(scenarios[0], BenchmarkerScenario)
        self.assertEqual(scenarios[0].output, 'json')

if __name__ == '__main__':
    unittest.main()
