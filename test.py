from muni_test import TestCase, TestRunner
runner = TestRunner()

runner.add_test_case(TestCase(
    description="Test Integer Declaration and Assignment",
    input_code="int a = 5; a;",
    expected_output="5"
))

runner.add_test_case(TestCase(
    description="Test Integer Addition",
    input_code="int a = 5; int b = 3; int sum = a + b; sum;",
    expected_output="8"
))

runner.add_test_case(TestCase(
    description="Test Integer Subtraction",
    input_code="int a = 5; int b = 3; int diff = a - b; diff;",
    expected_output="2"
))

runner.add_test_case(TestCase(
    description="Test Integer Multiplication",
    input_code="int a = 5; int b = 3; int prod = a * b; prod;",
    expected_output="15"
))


runner.add_test_case(TestCase(
    description="Test Integer Division",
    input_code="int a = 15; int b = 3; int div = a / b; div;",
    expected_output="5"
))

runner.add_test_case(TestCase(
    description="Test Integer Division",
    input_code="int a = 15; int b = 3; int div = a / b; div;",
    expected_output="5"
))

runner.add_test_case(TestCase(
    description="Test Division by Zero",
    input_code="int a = 5; int b = 0; int div = a / b; div;",
    expected_error="Error: Division by zero"
))

runner.add_test_case(TestCase(
    description="Test Negative Numbers Arithmetic",
    input_code="int a = -5; int b = 3; int sum = a + b; sum;",
    expected_output="-2"
))

runner.add_test_case(TestCase(
    description="Test Integer Increment",
    input_code="int a = 0; for(int i = 0; i < 5; i += 1;) { a += 1; } a;",
    expected_output="5"
))

runner.add_test_case(TestCase(
    description="Test Integer Comparison",
    input_code="int a = 5; int b = 3; a > b;",
    expected_output="true"
))



runner.run()