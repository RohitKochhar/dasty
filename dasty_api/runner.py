from .dasty import YAMLScenario
import pathlib

class ScenarioRunner():
    def __init__(self, directory_name, **kwargs):
        self.get_directory(directory_name)
        self.kwargs = kwargs

    def get_directory(self, directory_name):
        """
        Checks if the directory exists
        """
        if not pathlib.Path(directory_name).exists():
            raise Exception(f"Directory {directory_name} does not exist")
        else:
            self.directory = pathlib.Path(directory_name)

    def collect_scenarios(self):
        """
        Collects all the scenarios in the directory
        """
        # Get each file name in the target directory
        scenario_filepaths = [str(path) for path in self.directory.glob("*.yaml")]
        # Create a YAML scenario for each file
        self.scenarios = [YAMLScenario(filepath=filepath) for filepath in scenario_filepaths]

    def run(self):
        """
        Runs all the scenarios in the directory
        """
        self.collect_scenarios()
        for scenario in self.scenarios:
            scenario.run()
