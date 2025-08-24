import io
import re
from contextlib import redirect_stdout

# This test file assumes it will be run by a script in the parent `python` directory,
# which will handle the import path for `quanta_synapse`.
from quanta_synapse import QuantaSynapse

class BDDRunner:
    """
    A simple, custom-built BDD test runner.
    It parses a .feature file and executes its scenarios.
    """
    def __init__(self, feature_file_path):
        self.feature_file_path = feature_file_path
        self.scenarios_run = 0
        self.scenarios_passed = 0
        self.failures = []
        self.steps = {
            'Given': self.given,
            'When': self.when,
            'Then': self.then,
        }
        self.state = {}  # To hold state between steps (e.g., class instances)

    def given(self, statement):
        """Executes the 'Given' step."""
        if statement == "a new QuantaSynapse instance":
            # Suppress constructor's stdout during test setup
            with redirect_stdout(io.StringIO()):
                self.state['instance'] = QuantaSynapse()
        else:
            raise NotImplementedError(f"Step not defined: Given {statement}")

    def when(self, statement):
        """Executes the 'When' step."""
        self.state['output'] = None
        f = io.StringIO()
        with redirect_stdout(f):
            if statement == "the connect method is called":
                self.state['instance'].connect()
            elif statement == "the disconnect method is called":
                self.state['instance'].disconnect()
            else:
                raise NotImplementedError(f"Step not defined: When {statement}")
        self.state['output'] = f.getvalue().strip()

    def then(self, statement):
        """Executes the 'Then' step and performs assertions."""
        match = re.match(r'the output should be "(.*)"', statement)
        if match:
            expected_output = match.group(1)
            actual_output = self.state.get('output', '')
            assert actual_output == expected_output, f"Expected '{expected_output}', but got '{actual_output}'"
        else:
            raise NotImplementedError(f"Step not defined: Then {statement}")

    def run_scenario(self, scenario_name, steps):
        """Runs a single scenario and its steps."""
        self.scenarios_run += 1
        print(f"  Scenario: {scenario_name}")
        self.state = {}  # Reset state for each new scenario
        try:
            for step_type, statement in steps:
                print(f"    {step_type} {statement}")
                self.steps[step_type](statement)
            self.scenarios_passed += 1
            print("    -> PASS")
        except (AssertionError, NotImplementedError) as e:
            self.failures.append((scenario_name, str(e)))
            print(f"    -> FAIL: {e}")

    def run(self):
        """Parses and runs all scenarios in the feature file."""
        with open(self.feature_file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        current_scenario = None
        scenario_steps = []
        for line in lines:
            if line.startswith("Scenario:"):
                if current_scenario:
                    self.run_scenario(current_scenario, scenario_steps)
                current_scenario = line.replace("Scenario: ", "")
                scenario_steps = []
            elif any(line.startswith(kw) for kw in self.steps):
                step_type, statement = line.split(" ", 1)
                scenario_steps.append((step_type, statement))

        if current_scenario:  # Ensure the last scenario in the file is run
            self.run_scenario(current_scenario, scenario_steps)

    def get_summary(self):
        """Returns a formatted string of the BDD test results."""
        summary = []
        summary.append("\n--- BDD Test Summary ---")
        summary.append(f"Total scenarios run: {self.scenarios_run}")
        summary.append(f"Scenarios passed:  {self.scenarios_passed}")
        failures = self.scenarios_run - self.scenarios_passed
        summary.append(f"Scenarios failed:  {failures}")
        if failures > 0:
            summary.append("\nFailure Details:")
            for name, reason in self.failures:
                summary.append(f"  - {name}: {reason}")
        summary.append("------------------------")
        return "\n".join(summary), failures == 0

def run_bdd_tests():
    """
    Runs all BDD tests and prints a summary.
    Returns True if all tests pass, False otherwise.
    """
    print("Running BDD Tests...")
    # Assumes the test runner is started from the `python` directory
    feature_file = 'tests/features/quanta_synapse.feature'
    runner = BDDRunner(feature_file)
    runner.run()
    summary, all_passed = runner.get_summary()
    print(summary)
    return all_passed
