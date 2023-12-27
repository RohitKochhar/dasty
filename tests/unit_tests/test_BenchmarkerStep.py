import unittest
from unittest.mock import patch, MagicMock
from dasty_api.benchmarking.BenchmarkerStep import BenchmarkerStep
from requests.models import Response # type: ignore

class TestBenchmarkerStep(unittest.TestCase):
    def setUp(self):
        self.step = BenchmarkerStep(name="TestStep", method="GET", url="http://example.com", expected_status_code=200)

    def test_calculate_packet_size(self):
        # Testing with different types of packet content
        self.assertEqual(self.step._calculate_packet_size(None), 0)
        self.assertEqual(self.step._calculate_packet_size(b'bytes content'), len(b'bytes content'))
        self.assertEqual(self.step._calculate_packet_size({'key': 'value'}), len('{"key": "value"}'.encode('utf-8')))
        self.assertEqual(self.step._calculate_packet_size("string content"), len("string content".encode('utf-8')))

    @patch.object(BenchmarkerStep, '_prepare_request')
    @patch('dasty_api.utils.measure_time')
    @patch.object(BenchmarkerStep, '_make_request')
    @patch.object(BenchmarkerStep, '_validate_response')
    def test_call(self, mock_validate_response, mock_make_request, mock_measure_time, mock_prepare_request):
        mock_response = MagicMock(spec=Response)
        mock_response.content = b'response content'
        mock_make_request.return_value = mock_response
        mock_measure_time.return_value = (mock_response, '100ms')  # Mock return value

        stats = []
        variables = {'var1': 'value1'}
        updated_variables, updated_stats = self.step(variables, stats)

        self.assertEqual(updated_variables, variables)
        # Compare all elements except the 3rd (time field)
        expected_stats_without_time = ['GET', 'http://example.com', 0, 1256]
        actual_stats_without_time = updated_stats[0][:2] + updated_stats[0][3:]
        self.assertEqual(actual_stats_without_time, expected_stats_without_time)

if __name__ == '__main__':
    unittest.main()
