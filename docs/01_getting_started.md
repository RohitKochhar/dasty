# Getting Started with Dasty

Welcome to Dasty, a powerful tool for API testing and benchmarking. This guide will help you get started with setting up Dasty and running your first API scenarios.

## Installation

1. **Install Dasty**: Ensure that Dasty is installed in your environment. You can install it via pip (Python's package installer):

   ```bash
   pip install dasty
   ```

2. **Dependencies**: Make sure all dependencies are installed. Dasty typically requires packages like `requests`, `yaml`, and `tabulate`.

## Running Standard API Scenarios

To run standard API scenarios:

1. **Create Your Scenario File**: Write your API scenarios in a YAML file. Here's an example structure:

   ```yaml
   name: "Sample API Test"
   description: "A simple test scenario"
   steps:
   - name: "Get Request"
     method: "GET"
     url: "http://example.com/api"
     expected_status_code: 200
   ```

2. **Run the Scenario**: Use the `ScenarioRunner` to execute your scenarios.

   ```python
   from dasty import ScenarioRunner

   runner = ScenarioRunner(directory="path/to/your/scenarios")
   runner.run()
   ```

## Using the Benchmarking Feature

Dasty's benchmarking feature allows you to measure the performance of your API scenarios:

1. **Switch to Benchmarker**: Instead of using `ScenarioRunner`, use `Benchmarker`.

   ```python
   from dasty import Benchmarker

   benchmarker = Benchmarker(directory="path/to/your/scenarios")
   benchmarker.run()
   ```

2. **View Benchmark Results**: After running the scenarios, you will see an output like this:

   ```
   Add, Get, and Delete Users
   --------------------------
   METHOD    URL                                         TIME (ms)    REQUEST SIZE (bytes)    RESPONSE SIZE (bytes)
   --------  ----------------------------------------  -----------  ----------------------  -----------------------
   GET       http://127.0.0.1:2396/                           2.09                       0                        2
   GET       http://127.0.0.1:2396/users                      1.45                       0                       84
   ... (additional rows of data) ...
   ```

   This output includes the method, URL, time taken, request size, and response size for each API call in your scenario.

## Tips for Effective Use

- **Organize Your Scenarios**: Keep your scenarios organized in specific directories for easy management.
- **Understand the Metrics**: Familiarize yourself with the different metrics provided by the benchmarking feature, such as response times and payload sizes.
- **Test Under Realistic Conditions**: For the most accurate benchmarking results, test under conditions that closely mimic your production environment.
