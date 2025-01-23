import pytest
from pyveritas.suite import VeritasTestSuite

def test_suite_basic():
    def add(a, b): return a + b
    suite = VeritasTestSuite("Basic Math Suite")
    suite.test("Adding 2 and 3 should equal 5", lambda: add(2, 3) == 5)
    suite.run()
if __name__ == "__main__":
    pytest.main(["-v", "tests/test_suite.py"])

