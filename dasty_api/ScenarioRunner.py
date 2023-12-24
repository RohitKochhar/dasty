from pathlib import Path
from .YAMLScenario import YAMLScenario

# ScenarioRunner class ---------------------------------------------------------
class ScenarioRunner:
    def __init__(self, directory_name: str, tags=None, **kwargs):
        """
        Initializes the ScenarioRunner with a specific directory and optional tags.

        Args:
            directory_name (str): The name of the directory containing YAML scenarios.
            tags (list, optional): List of tags to filter which scenarios are run. If None, all scenarios are run.
            **kwargs: Additional keyword arguments that might be needed for future extensions.
        """
        self.directory = self._get_directory(directory_name)
        self.tags = tags
        self.kwargs = kwargs

    def _get_directory(self, directory_name: str) -> Path:
        """
        Verifies if the directory exists and returns a Path object.

        Args:
            directory_name (str): The name of the directory to check.

        Returns:
            Path: A Path object representing the directory.

        Raises:
            FileNotFoundError: If the directory does not exist.
        """
        directory_path = Path(directory_name)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory {directory_name} does not exist")
        return directory_path

    def _collect_scenarios(self) -> list:
        """
        Collects all the YAML scenarios in the directory and returns them.

        Returns:
            list: A list of YAMLScenario objects representing the scenarios found.
        """
        scenario_filepaths = self.directory.glob("*.yaml")
        return [YAMLScenario(filepath=str(filepath)) for filepath in scenario_filepaths]

    def run(self):
        """
        Runs all the collected scenarios. Scenarios are filtered based on the provided tags.
        """
        scenarios = self._collect_scenarios()
        for scenario in scenarios:
            if self._should_run_scenario(scenario):
                scenario.run()

    def _should_run_scenario(self, scenario: YAMLScenario) -> bool:
        """
        Collects all the YAML scenarios in the directory and returns them.

        Returns:
            list: A list of YAMLScenario objects representing the scenarios found.
        """
        if "ignore" in scenario.tags:
            print(f"Skipping scenario {scenario.name} due to 'ignore' tag.")
            return False
        if self.tags is None or any(tag in scenario.tags for tag in self.tags):
            return True
        print(f"Skipping scenario {scenario.name}; it lacks the required tags {self.tags}.")
        return False
