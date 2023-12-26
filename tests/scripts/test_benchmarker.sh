#!/bin/bash

# Start the server in the background
echo "Starting the server..."
python3 examples/simple_server.py > /dev/null 2>&1 &
SERVER_PID=$!

# Wait for the server to be fully up and running
# Adjust the sleep time as needed for your server's startup time
echo "Waiting for the server to initialize..."
sleep 1

# Run the Python file for Dasty tests
echo "Running Dasty tests..."
if [ "$SILENT" == "true" ]; then
    python3 tests/test_benchmarker.py > /dev/null 2>&1
else
    python3 tests/test_benchmarker.py
fi

# Optionally check the exit status of the Python script
if [ $? -ne 0 ]; then
    echo "Dasty tests failed."
    exit 1
else
    echo "Dasty tests completed successfully."
fi

# Shut down the server
echo "Shutting down the server..."
kill $SERVER_PID
