# ANSI escape codes for colors
RED=\033[0;31m
GREEN=\033[0;32m
NO_COLOR=\033[0m

test-scenarios:
	python3 -m tests.test_scenario_runner

run-test-suite:
	@echo "Running test suite..."
	@echo "---- Testing the scenario_runner ----"
	@SILENT=true sh ./tests/scripts/test_scenario_runner.sh
	@if [ $$? -ne 0 ]; then \
		echo "$(RED)Scenario runner test failed!$(NO_COLOR)"; \
		exit 1; \
	else \
		echo "$(GREEN)Scenario runner test complete$(NO_COLOR)"; \
	fi
	@echo "---- Testing the table benchmarker ----"
	@SILENT=true sh ./tests/scripts/test_benchmarker.sh
	@if [ $$? -ne 0 ]; then \
		echo "$(RED)Table benchmarker test failed!$(NO_COLOR)"; \
		exit 1; \
	else \
		echo "$(GREEN)Table benchmarker test complete$(NO_COLOR)"; \
	fi
	@echo "---- Testing the yaml benchmarker ----"
	@export SILENT=true; export OUTPUT_TYPE=yaml; sh ./tests/scripts/test_benchmarker.sh
	@if [ $$? -ne 0 ]; then \
		echo "$(RED)YAML benchmarker test failed!$(NO_COLOR)"; \
		exit 1; \
	else \
		echo "$(GREEN)YAML benchmarker test complete$(NO_COLOR)"; \
	fi
	@echo "---- Testing the json benchmarker ----"
	@export SILENT=true; export OUTPUT_TYPE=json; sh ./tests/scripts/test_benchmarker.sh
	@if [ $$? -ne 0 ]; then \
		echo "$(RED)JSON benchmarker test failed!$(NO_COLOR)"; \
		exit 1; \
	else \
		echo "$(GREEN)JSON benchmarker test complete$(NO_COLOR)"; \
	fi
	@echo "---- Testing the csv benchmarker ----"
	@export SILENT=true; export OUTPUT_TYPE=csv; sh ./tests/scripts/test_benchmarker.sh
	@if [ $$? -ne 0 ]; then \
		echo "$(RED)csv benchmarker test failed!$(NO_COLOR)"; \
		exit 1; \
	else \
		echo "$(GREEN)csv benchmarker test complete$(NO_COLOR)"; \
	fi
