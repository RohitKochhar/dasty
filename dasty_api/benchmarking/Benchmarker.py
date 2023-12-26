from ..ScenarioRunner import ScenarioRunner
from .BenchmarkingScenario import BenchmarkingScenario

class Benchmarker(ScenarioRunner):
    def __init__(self, directory_name: str, tags=None, output="table", **kwargs):
        """
        Initializes the Benchmarker with a specific directory and optional tags.

        Args:
            directory_name (str): The name of the directory containing YAML scenarios.
            tags (list, optional): List of tags to filter which scenarios are run. If None, all scenarios are run.
            **kwargs: Additional keyword arguments that might be needed for future extensions.
        """
        super().__init__(directory_name, tags, **kwargs)
        if output not in ["table", "csv", "json", "yaml"]:
            print(f"Output format \"{output}\" not supported. Defaulting to table.")
            output = "table"
        self.output = output

    def _collect_scenarios(self) -> list:
        """
        Collects all the YAML scenarios in the directory and returns them.

        Returns:
            list: A list of BenchmarkingScenario objects representing the scenarios found.
        """
        scenario_filepaths = self.directory.glob("*.yaml")
        return [BenchmarkingScenario(filepath=str(filepath), output=self.output) for filepath in scenario_filepaths]
