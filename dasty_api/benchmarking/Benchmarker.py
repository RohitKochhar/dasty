from ..ScenarioRunner import ScenarioRunner
from .BenchmarkingScenario import BenchmarkingScenario

class Benchmarker(ScenarioRunner):
    def _collect_scenarios(self) -> list:
        """
        Collects all the YAML scenarios in the directory and returns them.

        Returns:
            list: A list of BenchmarkingScenario objects representing the scenarios found.
        """
        scenario_filepaths = self.directory.glob("*.yaml")
        return [BenchmarkingScenario(filepath=str(filepath)) for filepath in scenario_filepaths]
