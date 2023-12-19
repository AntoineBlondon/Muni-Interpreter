import unittest
from math import sqrt
from muni_types import *

class TestMuniOperations(unittest.TestCase):
    def test_integer_addition(self):
        int1 = Muni_Int(5)
        int2 = Muni_Int(10)
        result = int1 + int2
        self.assertEqual(result.value, 15)

    def test_integer_subtraction(self):
        int1 = Muni_Int(15)
        int2 = Muni_Int(5)
        result = int1 - int2
        self.assertEqual(result.value, 10)

    def test_integer_multiplication(self):
        int1 = Muni_Int(5)
        int2 = Muni_Int(10)
        result = int1 * int2
        self.assertEqual(result.value, 50)

    def test_integer_truedivision(self):
        int1 = Muni_Int(10)
        int2 = Muni_Int(5)
        result = int1 / int2
        self.assertEqual(result.value, 2.0)

    def test_integer_floordivision(self):
        int1 = Muni_Int(10)
        int2 = Muni_Int(3)
        result = int1 // int2
        self.assertEqual(result.value, 3)

    def test_integer_modulus(self):
        int1 = Muni_Int(10)
        int2 = Muni_Int(3)
        result = int1 % int2
        self.assertEqual(result.value, 1)

    def test_integer_equality(self):
        int1 = Muni_Int(5)
        int2 = Muni_Int(5)
        self.assertTrue(int1 == int2)

    def test_integer_inequality(self):
        int1 = Muni_Int(5)
        int2 = Muni_Int(10)
        self.assertTrue(int1 != int2)

    def test_integer_less_than(self):
        int1 = Muni_Int(5)
        int2 = Muni_Int(10)
        self.assertTrue(int1 < int2)

    def test_integer_less_than_or_equal(self):
        int1 = Muni_Int(5)
        int2 = Muni_Int(5)
        self.assertTrue(int1 <= int2)

    def test_integer_greater_than(self):
        int1 = Muni_Int(10)
        int2 = Muni_Int(5)
        self.assertTrue(int1 > int2)

    def test_integer_greater_than_or_equal(self):
        int1 = Muni_Int(5)
        int2 = Muni_Int(5)
        self.assertTrue(int1 >= int2)

    def test_float_addition(self):
        float1 = Muni_Float(5.5)
        float2 = Muni_Float(3.5)
        result = float1 + float2
        self.assertAlmostEqual(result.value, 9.0)

    def test_float_subtraction(self):
        float1 = Muni_Float(5.5)
        float2 = Muni_Float(3.5)
        result = float1 - float2
        self.assertAlmostEqual(result.value, 2.0)

    def test_float_multiplication(self):
        float1 = Muni_Float(5.5)
        float2 = Muni_Float(3.5)
        result = float1 * float2
        self.assertAlmostEqual(result.value, 19.25)

    def test_float_truedivision(self):
        float1 = Muni_Float(10.0)
        float2 = Muni_Float(2.0)
        result = float1 / float2
        self.assertAlmostEqual(result.value, 5.0)

    def test_float_floordivision(self):
        float1 = Muni_Float(10.0)
        float2 = Muni_Float(3.0)
        result = float1 // float2
        self.assertAlmostEqual(result.value, 3.0)

    def test_float_modulus(self):
        float1 = Muni_Float(10.0)
        float2 = Muni_Float(3.0)
        result = float1 % float2
        self.assertAlmostEqual(result.value, 1.0)

    def test_float_equality(self):
        float1 = Muni_Float(5.5)
        float2 = Muni_Float(5.5)
        self.assertTrue(float1 == float2)

    def test_float_inequality(self):
        float1 = Muni_Float(5.5)
        float2 = Muni_Float(3.5)
        self.assertTrue(float1 != float2)

    def test_float_less_than(self):
        float1 = Muni_Float(3.5)
        float2 = Muni_Float(5.5)
        self.assertTrue(float1 < float2)

    def test_float_less_than_or_equal(self):
        float1 = Muni_Float(5.5)
        float2 = Muni_Float(5.5)
        self.assertTrue(float1 <= float2)

    def test_float_greater_than(self):
        float1 = Muni_Float(5.5)
        float2 = Muni_Float(3.5)
        self.assertTrue(float1 > float2)

    def test_float_greater_than_or_equal(self):
        float1 = Muni_Float(5.5)
        float2 = Muni_Float(5.5)
        self.assertTrue(float1 >= float2)

    def test_based_number_addition(self):
        based1 = Muni_BasedNumber("101", 2)
        based2 = Muni_BasedNumber("10", 2)
        result = based1.add(based2, 10)
        self.assertEqual(result.value, 7)  # In base 10

    def test_based_number_subtraction(self):
        based1 = Muni_BasedNumber("101", 2)
        based2 = Muni_BasedNumber("10", 2)
        result = based1.subtract(based2, 10)
        self.assertEqual(result.value, 3)  # In base 10

    def test_based_number_multiplication(self):
        based1 = Muni_BasedNumber("101", 2)
        based2 = Muni_BasedNumber("10", 2)
        result = based1.multiply(based2, 10)
        self.assertEqual(result.value, 10)  # In base 10

    def test_based_number_truedivision(self):
        based1 = Muni_BasedNumber("101", 2)
        based2 = Muni_BasedNumber("10", 2) 
        result = based1.divide(based2)
        self.assertEqual(result.value, 2.5)

    def test_based_number_equality(self):
        based1 = Muni_BasedNumber("101", 2)
        based2 = Muni_BasedNumber("5", 10)
        self.assertTrue(based1 == based2)

    def test_based_number_inequality(self):
        based1 = Muni_BasedNumber("101", 2)
        based2 = Muni_BasedNumber("10", 2)
        self.assertTrue(based1 != based2)

    def test_complex_addition(self):
        complex1 = Muni_Complex(1, 2)
        complex2 = Muni_Complex(2, 3)
        result = complex1 + complex2
        self.assertEqual(result.real, 3)
        self.assertEqual(result.imag, 5)

    def test_complex_modulus(self):
        complex1 = Muni_Complex(3, 4)
        result = complex1.modulus()
        self.assertAlmostEqual(result.value, 5.0)

    # Add similar test methods for subtraction, multiplication, division, etc.

    def test_division_by_zero(self):
        int1 = Muni_Int(5)
        int2 = Muni_Int(0)
        with self.assertRaises(ValueError):
            result = int1 / int2

    def test_modulus_by_zero(self):
        int1 = Muni_Int(5)
        int2 = Muni_Int(0)
        with self.assertRaises(ValueError):
            result = int1 % int2

    def test_based_number_invalid_base(self):
        with self.assertRaises(ValueError):
            based = Muni_BasedNumber("101", 1)

    # Add more test cases for edge cases and error handling as needed

if __name__ == '__main__':
    unittest.main()
