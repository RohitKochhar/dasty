from dasty_api import Benchmarker
import os

OUTPUT_TYPE = os.environ.get("OUTPUT_TYPE", "table")

if __name__ == "__main__":
    relative_path = os.path.dirname(__file__)
    print(relative_path)
    benchmarker = Benchmarker("./tests/test_scenarios", output=OUTPUT_TYPE)
    benchmarker.run()
