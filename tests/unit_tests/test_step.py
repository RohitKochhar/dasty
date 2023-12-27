import unittest
from unittest.mock import patch, MagicMock
from dasty_api.Step import Step  # Replace with your actual module name

class TestStep(unittest.TestCase):
    def setUp(self):
        self.get_step = Step(name="TestStepGET", method="GET", url="http://example.com", expected_status_code=200)
        self.post_step = Step(name="TestStepPOST", method="POST", url="http://example.com", expected_status_code=200, request_body={"key": "value"})

    def _mock_response(self, status_code=200, json_data=None, text_data=None):
        mock_response = MagicMock()
        mock_response.status_code = status_code
        if json_data is not None:
            mock_response.json.return_value = json_data
        if text_data is not None:
            mock_response.text = text_data
        return mock_response

    @patch('requests.get')
    def test_get_make_request_success(self, mock_get):
        mock_get.return_value = self._mock_response()
        response = self.get_step._make_request()
        mock_get.assert_called_with("http://example.com", headers={})
        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_post_make_request_success(self, mock_post):
        mock_post.return_value = self._mock_response()
        response = self.post_step._make_request()
        mock_post.assert_called_with("http://example.com", json={"key": "value"}, headers={})
        self.assertEqual(response.status_code, 200)
    def test_prepare_request_with_variables(self):
        variables = {"var1": "value1", "var2": 19}
        self.get_step.url = "http://example.com?param=${var1}"
        self.get_step.request_body = {"user": {"id": "${var2}"}}
        self.get_step._prepare_request(variables)
        self.assertEqual(self.get_step.url, "http://example.com?param=value1")
        self.assertEqual(self.get_step.request_body, {"user": {"id": "19"}})

    @patch('requests.get')
    def test_validate_response_with_json_success(self, mock_get):
        mock_get.return_value = self._mock_response(json_data={'key': 'value'})
        self.get_step.response_includes = {'key': 'value'}
        self.get_step.response_excludes = {'key': 'non-existent-value'}
        self.get_step.response_length = {'key': 5}
        variables = {}
        self.get_step._validate_response(mock_get.return_value, variables)

    @patch('requests.get')
    def test_validate_response_with_incorrect_json(self, mock_get):
        mock_get.return_value = self._mock_response(json_data={'key': 'incorrect value'})
        self.get_step.response_includes = {'key': 'value'}
        self.get_step.response_length = {'key': 10}
        variables = {}
        with self.assertRaises(AssertionError):
            self.get_step(variables)

    @patch('requests.get')
    def test_extract_data_and_output(self, mock_get):
        mock_get.return_value = self._mock_response(json_data={'user': {'id': 1234, 'name': 'John'}})
        self.get_step.extract = [{'from': 'user.id', 'name': 'userId'}]
        self.get_step.output = ['User ID: ${userId}']
        variables = {}
        self.get_step(variables)
        self.assertEqual(variables['userId'], 1234)

    @patch('requests.get')
    def test_verify_expectations_pass_and_fail(self, mock_get):
        mock_get.return_value = self._mock_response(json_data={'user': {'age': 30}})
        variables = {'user_age': 30}
        # Test case where expectations should pass
        self.get_step.expect = [{'variable': '${user_age}', 'operator': 'eq', 'value': '30'}]
        self.get_step(variables)

        # Test case where expectations should fail
        self.get_step.expect = [{'variable': '${user_age}', 'operator': 'ne', 'value': '30'}]
        with self.assertRaises(AssertionError):
            self.get_step(variables)
