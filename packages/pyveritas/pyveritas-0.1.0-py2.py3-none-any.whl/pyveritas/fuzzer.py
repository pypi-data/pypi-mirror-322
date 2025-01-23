# pyveritas/fuzzer.py
import random

class VeritasFuzzer:
    @staticmethod
    def choice(options):
        return random.choice(options)

    @staticmethod
    def float_range(min_val, max_val):
        return random.uniform(min_val, max_val)

    def __init__(self, function):
        self.function = function

    def run(self, input_spec, iterations=100):
        for i in range(iterations):
            inputs = {key: spec() for key, spec in input_spec.items()}
            try:
                self.function(**inputs)
                print(f"Fuzzing iteration {i+1}: PASSED with inputs {inputs}")
            except Exception as e:
                print(f"Fuzzing iteration {i+1}: FAILED with inputs {inputs} (Exception: {e})")

