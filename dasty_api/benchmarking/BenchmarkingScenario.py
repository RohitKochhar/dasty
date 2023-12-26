import csv
import json
import yaml # type: ignore
from io import StringIO
from ..Scenario import Scenario
from .BenchmarkerStep import BenchmarkerStep
from tabulate import tabulate # type: ignore

class BenchmarkingScenario(Scenario):
    def __init__(self, filepath: str, output="table") -> None:
        """
        Initializes a BenchmarkingScenario object by loading and parsing a YAML file.

        Args:
            filepath (str): The path to the YAML file containing the scenario definition.

        Raises:
            ValueError: If the YAML file is empty or essential fields are missing.
        """
        super().__init__(filepath)
        self.steps = [BenchmarkerStep(**step) for step in self.yaml_content.get('steps', [])]
        self.output = output

    def run(self) -> None:
        """
        Executes all the steps defined in the scenario.
        """
        stats = []
        for step in self.steps:
            try:
                step(self.variables, stats)
            except Exception as e:
                print(f"Error occurred in step execution: {e}")
                return
        self._display_output(stats)

    def _display_output(self, stats):
        headers = ["method", "url", "time_ms", "request_size", "response_size"]
        if self.output == "table":
            self._print_table(stats, headers)
        elif self.output == "csv":
            print(self._to_csv(stats, headers))
        elif self.output == "json":
            print(self._to_json(stats, headers))
        elif self.output == "yaml":
            print(self._to_yaml(stats, headers))

    def _print_table(self, stats, headers):
        print(f"\n{self.name}\n" + "-" * len(self.name))
        print(tabulate(stats, headers=headers))

    def _to_csv(self, data, headers):
        """ Converts data to CSV format. """
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Scenario", self.name])
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
        return output.getvalue()

    def _to_json(self, data, headers):
        """ Converts data to JSON format. """
        json_data = [dict(zip(headers, row)) for row in data]
        return json.dumps({"scenario_name": self.name, "stats": json_data}, indent=4)

    def _to_yaml(self, data, headers):
        """ Converts data to YAML format. """
        yaml_data = [dict(zip(headers, row)) for row in data]
        return yaml.dump({"scenario_name": self.name, "stats": yaml_data}, default_flow_style=False)
