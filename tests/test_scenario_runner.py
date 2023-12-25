from dasty_api.ScenarioRunner import ScenarioRunner

if __name__ == "__main__":
    timed_runner = ScenarioRunner("./examples/scenarios", time=True)
    untimed_runner = ScenarioRunner("./examples/scenarios")
    timed_runner.run()
    untimed_runner.run()
