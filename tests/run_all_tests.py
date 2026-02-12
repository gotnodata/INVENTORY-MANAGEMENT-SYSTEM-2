import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests():
    """Discover and run all tests"""
    # Discover all test files
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    print("Running Inventory Management System Tests")
    print("=" * 50)
    
    exit_code = run_tests()
    
    print("\n" + "=" * 50)
    if exit_code == 0:
        print("All tests passed!")
    else:
        print("Some tests failed!")
    
    sys.exit(exit_code)
