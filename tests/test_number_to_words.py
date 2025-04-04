import unittest
from to_test.number_to_words import number_to_words

class TestNumberToWords(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(number_to_words(0), "Zero")

    def test_single_digit(self):
        self.assertEqual(number_to_words(1), "One")
        self.assertEqual(number_to_words(5), "Five")
        self.assertEqual(number_to_words(9), "Nine")

    def test_teens(self):
        self.assertEqual(number_to_words(10), "Ten")
        self.assertEqual(number_to_words(11), "Eleven")
        self.assertEqual(number_to_words(12), "Twelve")
        self.assertEqual(number_to_words(19), "Nineteen")

    def test_tens(self):
        self.assertEqual(number_to_words(20), "Twenty")
        self.assertEqual(number_to_words(30), "Thirty")
        self.assertEqual(number_to_words(90), "Ninety")

    def test_two_digits(self):
        self.assertEqual(number_to_words(21), "Twenty One")
        self.assertEqual(number_to_words(57), "Fifty Seven")
        self.assertEqual(number_to_words(99), "Ninety Nine")

    def test_hundreds(self):
        self.assertEqual(number_to_words(100), "One Hundred")
        self.assertEqual(number_to_words(300), "Three Hundred")
        self.assertEqual(number_to_words(900), "Nine Hundred")

    def test_hundreds_with_tens_and_ones(self):
        self.assertEqual(number_to_words(101), "One Hundred One")
        self.assertEqual(number_to_words(110), "One Hundred Ten")
        self.assertEqual(number_to_words(111), "One Hundred Eleven")
        self.assertEqual(number_to_words(120), "One Hundred Twenty")
        self.assertEqual(number_to_words(121), "One Hundred Twenty One")
        self.assertEqual(number_to_words(345), "Three Hundred Forty Five")
        self.assertEqual(number_to_words(999), "Nine Hundred Ninety Nine")

    def test_thousands(self):
        self.assertEqual(number_to_words(1000), "One Thousand")
        self.assertEqual(number_to_words(2000), "Two Thousand")
        self.assertEqual(number_to_words(12345), "Twelve Thousand Three Hundred Forty Five")

    def test_millions(self):
        self.assertEqual(number_to_words(1000000), "One Million")
        self.assertEqual(number_to_words(1234567), "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven")

    def test_billions(self):
        self.assertEqual(number_to_words(1000000000), "One Billion")
        self.assertEqual(number_to_words(1234567890), "One Billion Two Hundred Thirty Four Million Five Hundred Sixty Seven Thousand Eight Hundred Ninety")

    def test_large_number(self):
         self.assertEqual(number_to_words(1234567890123), "One Trillion Two Hundred Thirty Four Billion Five Hundred Sixty Seven Million Eight Hundred Ninety Thousand One Hundred Twenty Three")

    def test_numbers_with_leading_zeros_in_triplets(self):
        self.assertEqual(number_to_words(1001), "One Thousand One")
        self.assertEqual(number_to_words(1010), "One Thousand Ten")
        self.assertEqual(number_to_words(1100), "One Thousand One Hundred")
        self.assertEqual(number_to_words(10000), "Ten Thousand")
        self.assertEqual(number_to_words(100000), "One Hundred Thousand")
        self.assertEqual(number_to_words(1000000), "One Million")
        self.assertEqual(number_to_words(10000000), "Ten Million")
        self.assertEqual(number_to_words(100000000), "One Hundred Million")

if __name__ == '__main__':
    unittest.main()