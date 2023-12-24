# Imports ---------------------------------------------------------------------
# Standard library imports
from pathlib import Path
# Local imports
from .YAMLScenario import YAMLScenario

class ScenarioRunner:
    def __init__(self, directory_name: str, tags=None, **kwargs):
        self.directory = self._get_directory(directory_name)
        self.tags = tags
        self.kwargs = kwargs

    def _get_directory(self, directory_name: str) -> Path:
        """
        Verifies if the directory exists and returns a Path object.
        """
        directory_path = Path(directory_name)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory {directory_name} does not exist")
        return directory_path

    def _collect_scenarios(self) -> list:
        """
        Collects all the YAML scenarios in the directory.
        """
        scenario_filepaths = self.directory.glob("*.yaml")
        return [YAMLScenario(filepath=str(filepath)) for filepath in scenario_filepaths]

    def run(self):
        """
        Runs all the scenarios in the directory.
        """
        scenarios = self._collect_scenarios()
        for scenario in scenarios:
            if self._should_run_scenario(scenario):
                scenario.run()

    def _should_run_scenario(self, scenario: YAMLScenario) -> bool:
        """
        Determines if a scenario should be run based on its tags.
        """
        if "ignore" in scenario.tags:
            print(f"Skipping scenario {scenario.name} due to 'ignore' tag.")
            return False
        if self.tags is None or any(tag in scenario.tags for tag in self.tags):
            return True
        print(f"Skipping scenario {scenario.name}; it lacks the required tags {self.tags}.")
        return False
