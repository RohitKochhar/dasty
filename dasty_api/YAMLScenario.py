# Imports ---------------------------------------------------------------------
# Standard library imports
import yaml # type: ignore
# Local application imports
from .Step import Step

# YAMLScenario class -----------------------------------------------------------
class YAMLScenario:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        with open(filepath, 'r') as f:
            yaml_content = yaml.safe_load(f)
        if yaml_content is None:
            raise ValueError(f"File {filepath} is empty")
        self.variables = yaml_content.get('variables', {})
        self.name = yaml_content['name']
        self.description = yaml_content['description']
        try:
            self.tags = yaml_content['tags']
        except KeyError:
            self.tags = []
        self.steps = [Step(**step) for step in yaml_content['steps']]

    def run(self) -> None:
        print(f"Running scenario {self.name} defined in {self.filepath}...")
        for step in self.steps:
            self.variables = step(self.variables)
        print("\033[92m" + f"{self.name} Success ✅" + "\033[0m")
