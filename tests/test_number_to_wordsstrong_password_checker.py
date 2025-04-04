import unittest
from to_test.strong_password_checker import strong_password_checker

class TestStrongPasswordChecker(unittest.TestCase):

    def test_empty_string(self):
        self.assertEqual(strong_password_checker(""), 6)

    def test_short_string_missing_requirements(self):
        self.assertEqual(strong_password_checker("a1"), 4)

    def test_short_string_some_requirements(self):
        self.assertEqual(strong_password_checker("aA1"), 0)

    def test_short_string_only_lowercase(self):
        self.assertEqual(strong_password_checker("aaaaa"), 2)

    def test_short_string_only_uppercase(self):
        self.assertEqual(strong_password_checker("AAAAA"), 2)

    def test_short_string_only_digits(self):
        self.assertEqual(strong_password_checker("11111"), 2)

    def test_short_string_with_repetition(self):
        self.assertEqual(strong_password_checker("aaa111"), 3)

    def test_medium_string_missing_requirements(self):
        self.assertEqual(strong_password_checker("aaaaaaa"), 3)

    def test_medium_string_with_repetition(self):
        self.assertEqual(strong_password_checker("aaabbb123"), 2)

    def test_medium_string_meets_requirements(self):
        self.assertEqual(strong_password_checker("aA12345"), 0)

    def test_long_string_missing_requirements(self):
        self.assertEqual(strong_password_checker("aaaaaaaaaaaaaaaaaaaaa"), 5)

    def test_long_string_with_repetition(self):
        self.assertEqual(strong_password_checker("aaaAAAbbbBBBc11111"), 8)

    def test_long_string_meets_requirements(self):
        self.assertEqual(strong_password_checker("aA1aA1aA1aA1aA1aA1aA1"), 1)

    def test_example_1(self):
        self.assertEqual(strong_password_checker("a"), 5)

    def test_example_2(self):
        self.assertEqual(strong_password_checker("aA1"), 0)

    def test_example_3(self):
        self.assertEqual(strong_password_checker("1337C0d3"), 0)

    def test_example_4(self):
        self.assertEqual(strong_password_checker("aaaaaaaAAAAAAA123456"), 3)

    def test_long_password_with_repeating_chars(self):
        self.assertEqual(strong_password_checker("ABABABABABABABABABAB"), 2)

    def test_long_password_with_repeating_chars_and_missing_digit(self):
        self.assertEqual(strong_password_checker("aaaaaaaaaaaaaaaaaaAA"), 6)

    def test_long_password_with_repeating_chars_near_limit(self):
        self.assertEqual(strong_password_checker("aaaaaaaaaaaaaaaaaaA1"), 5)

    def test_long_password_with_repeating_chars_and_missing_uppercase(self):
        self.assertEqual(strong_password_checker("111111111111111111aa"), 6)
    
    def test_long_password_with_repeating_chars_and_all_missing(self):
        self.assertEqual(strong_password_checker("aaaaaaaaaaaaaaaaaaaaaa"), 6)


if __name__ == '__main__':
    unittest.main()