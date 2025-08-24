import sys

# By running this script from within the `python` directory, the current
# directory is automatically added to the Python path. This allows the
# script to find and import modules from the `tests` and `quanta_synapse`
# packages, which are located in the same directory.
from tests.test_unit import run_unit_tests
from tests.test_bdd import run_bdd_tests

def main():
    """
    Runs all unit and BDD tests and reports a final summary.
    """
    print("=========================")
    print("= Running Test Suite    =")
    print("=========================\n")

    # Run unit tests
    unit_tests_passed = run_unit_tests()

    print("\n" + "="*30 + "\n") # Spacer

    # Run BDD tests
    bdd_tests_passed = run_bdd_tests()

    print("\n=========================")
    print("= Test Suite Complete   =")
    print("=========================")

    if unit_tests_passed and bdd_tests_passed:
        print("\nSUCCESS: All tests passed!")
        sys.exit(0)
    else:
        print("\nFAILURE: Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
