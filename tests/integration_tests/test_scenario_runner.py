from dasty_api.ScenarioRunner import ScenarioRunner
import os

if __name__ == "__main__":
    scenarios_path = os.path.dirname(__file__) + "/test_scenarios"
    runner = ScenarioRunner(scenarios_path)
    runner.run()
