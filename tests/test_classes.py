from dasty_api import ScenarioRunner, Benchmarker

if __name__ == "__main__":
    runner = ScenarioRunner("./examples/scenarios")
    runner.run()
    benchmarker = Benchmarker("./tests/benchmarks")
    benchmarker.run()
