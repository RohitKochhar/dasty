# ANSI escape codes for colors
RED=\033[0;31m
GREEN=\033[0;32m
NO_COLOR=\033[0m

# Function to run a test
# Arguments:
#   1 - Test Type (ScenarioRunner or Benchmarker)
#   2 - Output Type (NA, table, yaml, json, csv)
#   3 - Silent Mode (true or false)
define run_test
	@echo "---- Testing the $(1) $(2) ----"
	@SILENT=$(3) sh ./tests/integration_tests/scripts/integration_test_runner.sh $(1) $(2)
	@if [ $$? -ne 0 ]; then \
		echo "$(RED)$(1) $(2) test failed!$(NO_COLOR)"; \
		exit 1; \
	else \
		echo "$(GREEN)$(1) $(2) test complete$(NO_COLOR)"; \
	fi
endef

integration-test-scenario-runner:
	$(call run_test,ScenarioRunner,NA,false)

integration-test-yaml-benchmark:
	$(call run_test,Benchmarker,yaml,false)

integration-test-json-benchmark:
	$(call run_test,Benchmarker,json,false)

integration-test-csv-benchmark:
	$(call run_test,Benchmarker,csv,false)

integration-test-table-benchmark:
	$(call run_test,Benchmarker,table,false)

run-test-suite:
	@echo "Running test suite..."
	$(call run_test,ScenarioRunner,NA,true)
	$(call run_test,Benchmarker,table,true)
	$(call run_test,Benchmarker,yaml,true)
	$(call run_test,Benchmarker,json,true)
	$(call run_test,Benchmarker,csv,true)

cov-gen:
	@echo "Generating coverage report..."
	coverage run -m unittest
	coverage report
	coverage html
