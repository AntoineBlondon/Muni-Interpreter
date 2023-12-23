from run import run

class TestCase:
    def __init__(self, description, input_code, expected_output=None, expected_error=None):
        self.description = description
        self.input_code = input_code
        self.expected_output = expected_output
        self.expected_error = expected_error

class TestRunner:
    def __init__(self):
        self.test_cases = []

    def add_test_case(self, test_case):
        self.test_cases.append(test_case)

    def run(self):
        for test in self.test_cases:
            try:
                output = execute_code(test.input_code)
                if test.expected_error:
                    print(f"FAIL {test.description}: Expected error, but got output.")
                elif output[-1] != test.expected_output:
                    print(f"FAIL {test.description}: Expected {test.expected_output}, got {output}.")
                else:
                    print(f"PASS {test.description}")
            except Exception as e:
                if test.expected_error and str(e) == test.expected_error:
                    print(f"PASS {test.description} (error expected)")
                else:
                    print(f"FAIL {test.description}: {e}")

def execute_code(code):
    return list(run(code))

