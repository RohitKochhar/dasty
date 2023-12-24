# Imports ---------------------------------------------------------------------
# Standard library imports
from pathlib import Path
# Local application imports
from .YAMLScenario import YAMLScenario

# ScenarioRunner class -----------------------------------------------------------
class ScenarioRunner():
    def __init__(self, directory_name, tags=None, **kwargs):
        self.get_directory(directory_name)
        self.tags = tags
        self.kwargs = kwargs

    def get_directory(self, directory_name):
        """
        Checks if the directory exists
        """
        if not Path(directory_name).exists():
            raise Exception(f"Directory {directory_name} does not exist")
        else:
            self.directory = Path(directory_name)

    def collect_scenarios(self):
        """
        Collects all the scenarios in the directory
        """
        scenario_filepaths = [str(path) for path in self.directory.glob("*.yaml")]
        self.scenarios = [YAMLScenario(filepath=filepath) for filepath in scenario_filepaths]

    def run(self):
        """
        Runs all the scenarios in the directory
        """
        self.collect_scenarios()
        for scenario in self.scenarios:
            if "ignore" in scenario.tags:
                print(f"Skipping scenario {scenario.name} because it has the tag 'ignore'")
                continue
            # If no tag was specified for the runner, run all tests
            if self.tags is None:
                scenario.run()
            else:
                # If tags were provided, check if the scenario has any of them
                if any(tag in scenario.tags for tag in self.tags):
                    scenario.run()
                else:
                    print(f"Skipping scenario {scenario.name} because it does not have any of the tags {self.tags}")
