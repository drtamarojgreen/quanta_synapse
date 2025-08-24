import io
from contextlib import redirect_stdout

# This test file assumes it will be run by a script in the parent `python` directory,
# which will handle the import path for `quanta_synapse`.
from quanta_synapse import QuantaSynapse

class SimpleUnitTester:
    """
    A simple, custom-built unit testing harness.
    It runs test functions and reports a summary of passes and failures.
    """
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.failures = []

    def run_test(self, test_func):
        """Runs a single test function and records its result."""
        self.tests_run += 1
        try:
            test_func()
            self.tests_passed += 1
            print(f"  - PASS: {test_func.__name__}")
        except AssertionError as e:
            self.failures.append((test_func.__name__, str(e)))
            print(f"  - FAIL: {test_func.__name__}")

    def get_summary(self):
        """Returns a formatted string of the test results."""
        summary = []
        summary.append("\n--- Unit Test Summary ---")
        summary.append(f"Total tests run: {self.tests_run}")
        summary.append(f"Tests passed:  {self.tests_passed}")
        failures = self.tests_run - self.tests_passed
        summary.append(f"Tests failed:  {failures}")
        if failures > 0:
            summary.append("\nFailure Details:")
            for name, reason in self.failures:
                summary.append(f"  - {name}: {reason}")
        summary.append("-------------------------")
        return "\n".join(summary), failures == 0

# --- Test Cases ---

def test_constructor_output():
    """Verifies that creating a QuantaSynapse instance prints the correct message."""
    f = io.StringIO()
    with redirect_stdout(f):
        _ = QuantaSynapse()
    output = f.getvalue().strip()
    assert output == "QuantaSynapse constructor", f"Expected 'QuantaSynapse constructor', but got '{output}'"

def test_connect_method_output():
    """Verifies that the connect() method prints the correct message."""
    # Suppress constructor output for this test
    with redirect_stdout(io.StringIO()):
        qs = QuantaSynapse()

    f_capture = io.StringIO()
    with redirect_stdout(f_capture):
        qs.connect()
    output = f_capture.getvalue().strip()
    assert output == "Connecting to Quanta projects...", f"Expected 'Connecting to Quanta projects...', but got '{output}'"

def test_disconnect_method_output():
    """Verifies that the disconnect() method prints the correct message."""
    # Suppress constructor output for this test
    with redirect_stdout(io.StringIO()):
        qs = QuantaSynapse()

    f_capture = io.StringIO()
    with redirect_stdout(f_capture):
        qs.disconnect()
    output = f_capture.getvalue().strip()
    assert output == "Disconnecting from Quanta projects...", f"Expected 'Disconnecting from Quanta projects...', but got '{output}'"

def run_unit_tests():
    """
    Runs all defined unit tests and prints a summary.
    Returns True if all tests pass, False otherwise.
    """
    tester = SimpleUnitTester()
    print("Running Unit Tests...")

    tests_to_run = [
        test_constructor_output,
        test_connect_method_output,
        test_disconnect_method_output,
    ]

    for t in tests_to_run:
        tester.run_test(t)

    summary, all_passed = tester.get_summary()
    print(summary)
    return all_passed
