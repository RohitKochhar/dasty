from dasty_api import Benchmarker
import os

OUTPUT_TYPE = os.environ.get("OUTPUT_TYPE", "table")

if __name__ == "__main__":
    scenarios_path = os.path.dirname(__file__) + "/test_scenarios"
    benchmarker = Benchmarker(scenarios_path, output=OUTPUT_TYPE)
    benchmarker.run()
