# import unittest
# from unittest.mock import patch, MagicMock
# from dasty_api.Step import Step  # Replace with the actual module name

# class TestStep(unittest.TestCase):

#     def setUp(self):
#         # Set up a test instance of Step
#         self.step = Step(name="TestStep", method="GET", url="http://example.com", expected_status_code=200)

#     @patch('requests.get')
#     def test_make_request(self, mock_get):
#         # Mock the GET request
#         mock_response = MagicMock()
#         mock_response.status_code = 200
#         mock_get.return_value = mock_response

#         # Call the _make_request method
#         response = self.step._make_request()

#         # Assert that the request was made correctly
#         mock_get.assert_called_with("http://example.com", headers={})
#         self.assertEqual(response.status_code, 200)

#     def test_prepare_request(self):
#         # Prepare variables
#         variables = {"var1": "value1"}

#         # Modify the URL to include a variable
#         self.step.url = "http://example.com?param={var1}"
#         self.step._prepare_request(variables)

#         # Assert that the URL was correctly replaced with the variable
#         self.assertEqual(self.step.url, "http://example.com?param=value1")

#     # def test_prepare_request(self):
#     #     # Prepare variables
#     #     variables = {"var1": "value1"}

#     #     # Modify the URL to include a variable
#     #     self.step.url = "http://example.com?param={var1}"
#     #     self.step._prepare_request(variables)

#     #     # Assert that the URL was correctly replaced with the variable
#     #     self.assertEqual(self.step.url, "http://example.com?param=value1")

#     # # Additional tests for other methods...

# if __name__ == '__main__':
#     unittest.main()
