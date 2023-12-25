import yaml # type: ignore
from .Step import Step
from .utils import measure_time

class Scenario:
    def __init__(self, filepath: str) -> None:
        """
        Initializes a Scenario object by loading and parsing a YAML file.

        Args:
            filepath (str): The path to the YAML file containing the scenario definition.

        Raises:
            ValueError: If the YAML file is empty or essential fields are missing.
        """
        self.filepath = filepath
        with open(filepath, 'r') as file:
            self.yaml_content = yaml.safe_load(file)

        if not self.yaml_content:
            raise ValueError(f"File {filepath} is empty or invalid YAML.")

        self.name = self.yaml_content.get('name')
        self.description = self.yaml_content.get('description')
        self.tags = self.yaml_content.get('tags', [])
        self.variables = self.yaml_content.get('variables', {})
        self.steps = [Step(**step) for step in self.yaml_content.get('steps', [])]

        self._validate_scenario()

    def run(self) -> None:
        """
        Executes all the steps defined in the scenario.
        """
        print(f"Running scenario {self.name} defined in {self.filepath}...")
        def run_steps():
            for step in self.steps:
                self.variables = step(self.variables)
        _, time_ms = measure_time(run_steps)
        print("\033[92m" + f"{self.name} Success ✅ ({time_ms}ms)\033[0m")

    def _validate_scenario(self) -> None:
        """
        Validates that the scenario has all the necessary attributes.

        Raises:
            ValueError: If essential attributes like name or steps are missing.
        """
        if not self.name:
            raise ValueError("Scenario name is required.")
        if not self.steps:
            raise ValueError("Scenario steps are required.")
