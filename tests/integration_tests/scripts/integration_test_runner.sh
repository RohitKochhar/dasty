#!/bin/bash

# Function to start the server silently
start_server() {
    if [ "$SILENT" == "true" ]; then
        python3 examples/simple_server.py > /dev/null 2>&1 &
    else
        echo "Starting the server..."
        python3 examples/simple_server.py > /dev/null 2>&1 &
    fi
    SERVER_PID=$!
    if [ "$SILENT" != "true" ]; then
        echo "Waiting for the server to initialize..."
    fi
    sleep 1  # Adjust the sleep time as needed
}

# Function to stop the server
stop_server() {
    if [ "$SILENT" != "true" ]; then
        echo "Shutting down the server..."
    fi
    kill $SERVER_PID
}

# Function to run a test script
run_test_script() {
    local test_type=$1
    local output_type=$2
    local script_name=""

    # Determine which script to run based on the first argument
    case $test_type in
        "ScenarioRunner")
            script_name="test_scenario_runner.py"
            ;;
        "Benchmarker")
            script_name="test_benchmarker.py"
            ;;
        *)
            if [ "$SILENT" != "true" ]; then
                echo "Invalid test type. Use 'ScenarioRunner' or 'Benchmarker'."
            fi
            exit 1
            ;;
    esac

    # Set the OUTPUT_TYPE environment variable
    export OUTPUT_TYPE=$output_type

    if [ "$SILENT" != "true" ]; then
        echo "Running $script_name tests with output format $output_type..."
    fi

    # Execute the test script silently if SILENT is true
    if [ "$SILENT" == "true" ]; then
        python3 tests/integration_tests/$script_name > /dev/null 2>&1
    else
        python3 tests/integration_tests/$script_name
    fi

    # Check the exit status
    if [ $? -ne 0 ]; then
        if [ "$SILENT" != "true" ]; then
            echo "$script_name tests failed."
        fi
        exit 1
    elif [ "$SILENT" != "true" ]; then
        echo "$script_name tests completed successfully."
    fi
}

# Main execution starts here
if [ "$#" -ne 2 ]; then
    if [ "$SILENT" != "true" ]; then
        echo "Usage: $0 <ScenarioRunner|Benchmarker> <output_type>"
    fi
    exit 1
fi

TEST_TYPE=$1
OUTPUT_TYPE=$2

start_server
run_test_script $TEST_TYPE $OUTPUT_TYPE
stop_server
