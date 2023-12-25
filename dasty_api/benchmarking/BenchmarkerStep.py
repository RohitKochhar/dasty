from ..Step import Step
import json
from ..utils import measure_time

class BenchmarkerStep(Step):
    def __call__(self, variables, stats) -> dict:
        """
        Executes the step by preparing the request, making the request, and validating the response.

        Args:
            variables (dict): Dictionary of variables to be used in this step.

        Returns:
            dict: Updated variables after extracting new ones from the response.
        """
        super()._prepare_request(variables)
        
        request_size = self._calculate_packet_size(self.request_body)
        response, time_ms = measure_time(super()._make_request)
        response_size = self._calculate_packet_size(response.content)

        super()._validate_response(response, variables)

        stats.append([self.method, self.url, time_ms, request_size, response_size])
        return variables, stats

    def _calculate_packet_size(self, packet):
        if packet is None:
            return 0
        
        if isinstance(packet, bytes):
            return len(packet)

        return len(json.dumps(packet).encode('utf-8')) if isinstance(packet, (dict, list)) \
            else len(str(packet).encode('utf-8'))
