from ..Scenario import Scenario
from .BenchmarkerStep import BenchmarkerStep
from tabulate import tabulate # type: ignore

class BenchmarkingScenario(Scenario):
    def __init__(self, filepath: str) -> None:
        """
        Initializes a BenchmarkingScenario object by loading and parsing a YAML file.

        Args:
            filepath (str): The path to the YAML file containing the scenario definition.

        Raises:
            ValueError: If the YAML file is empty or essential fields are missing.
        """
    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        self.steps = [BenchmarkerStep(**step) for step in self.yaml_content.get('steps', [])]

    def run(self) -> None:
        """
        Executes all the steps defined in the scenario.
        """
        print(f"\n{self.name}\n" + "-" * len(self.name))
        stats = []
        for step in self.steps:
            step(self.variables, stats)
        print(tabulate(stats, headers=["METHOD", "URL", "TIME (ms)", "REQUEST SIZE (bytes)", "RESPONSE SIZE (bytes)"]))
