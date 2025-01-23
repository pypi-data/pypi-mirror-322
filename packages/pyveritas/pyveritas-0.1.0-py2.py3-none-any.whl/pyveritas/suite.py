# pyveritas/suite.py
class VeritasTestSuite:
    def __init__(self, name):
        self.name = name
        self.tests = []

    def test(self, description, test_function, should_raise=None):
        self.tests.append((description, test_function, should_raise))

    def run(self):
        print(f"Running test suite: {self.name}")
        for i, (desc, func, should_raise) in enumerate(self.tests, 1):
            try:
                func()
                if should_raise:
                    print(f"Test {i} FAILED: {desc} (Exception was expected but not raised)")
                else:
                    print(f"Test {i} PASSED: {desc}")
            except Exception as e:
                if should_raise and isinstance(e, should_raise):
                    print(f"Test {i} PASSED: {desc} (Expected exception raised: {e})")
                else:
                    print(f"Test {i} FAILED: {desc} (Unexpected exception: {e})")

