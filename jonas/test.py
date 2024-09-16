import unittest
from jonas_file import line_lengths

class TestLineLengths(unittest.TestCase):
    def test_empty_text(self):
        text = ""
        self.assertEqual(line_lengths(text), [0])

    def test_single_line(self):
        text = "Hello, world!"
        self.assertEqual(line_lengths(text), [13])

    def test_multiple_lines(self):
        text = "This is line 1.\nLine 2 is longer.\nLine 3 is the shortest."
        self.assertEqual(line_lengths(text), [15, 17, 23])

    def test_whitespace(self):
        text = "   Leading whitespace.\nTrailing whitespace.   "
        self.assertEqual(line_lengths(text), [22, 23])

    def test_empty_lines(self):
        text = "Line 1\n\nLine 3"
        self.assertEqual(line_lengths(text), [6, 0, 6])

    def test_invalid_input(self):
        text = 42
        self.assertRaises(TypeError, line_lengths, text)

if __name__ == '__main__':
    unittest.main()

# the non-verbose version of 'git log' is 'git log --oneline'
s