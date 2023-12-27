import unittest
from unittest.mock import patch, MagicMock
from dasty_api.benchmarking.BenchmarkerScenario import BenchmarkerScenario
from dasty_api.benchmarking.BenchmarkerStep import BenchmarkerStep
from io import StringIO

class TestBenchmarkerScenario(unittest.TestCase):
    def setUp(self):
        self.filepath = './tests/integration_tests/test_scenarios/healthchecks.yaml'
        self.output_format = 'table'

    @patch('dasty_api.Scenario.__init__')
    def test_init(self, mock_scenario_init):
        mock_scenario_init.return_value = None
        scenario = BenchmarkerScenario(self.filepath, output=self.output_format)
        self.assertEqual(scenario.output, self.output_format)

    @patch.object(BenchmarkerScenario, '_display_output')
    @patch.object(BenchmarkerStep, '__call__')
    def test_run(self, mock_step_call, mock_display_output):
        mock_step_call.return_value = ({}, [])
        scenario = BenchmarkerScenario(self.filepath, output=self.output_format)
        scenario.steps = [MagicMock(spec=BenchmarkerStep)] * 2
        scenario.run()

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_output_table(self, mock_stdout):
        scenario = BenchmarkerScenario(self.filepath, output='table')
        stats = [['GET', 'http://example.com', '100ms', 100, 200]]
        scenario._display_output(stats)
        self.assertIn('GET', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_output_csv(self, mock_stdout):
        scenario = BenchmarkerScenario(self.filepath, output='csv')
        stats = [['GET', 'http://example.com', '100ms', 100, 200]]
        scenario._display_output(stats)
        self.assertIn('GET', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_output_json(self, mock_stdout):
        scenario = BenchmarkerScenario(self.filepath, output='json')
        stats = [['GET', 'http://example.com', '100ms', 100, 200]]
        scenario._display_output(stats)
        self.assertIn('http://example.com', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_output_yaml(self, mock_stdout):
        scenario = BenchmarkerScenario(self.filepath, output='yaml')
        stats = [['GET', 'http://example.com', '100ms', 100, 200]]
        scenario._display_output(stats)
        self.assertIn('http://example.com', mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
