import itertools
import os
import re
import unittest
from tempfile import TemporaryDirectory

import lineinfile


class TestGetRegex(unittest.TestCase):

    def test_match(self):
        regex = lineinfile.get_regex("TEST=")
        whitespaces = ["", " ", "  ", "\t", " \t", "\t ", " \t "]
        should_match = [
            whitespaces,
            ["", "#", "//"],
            whitespaces,
            ["TEST="],
            ["", "123"],
        ]
        for expected in itertools.product(*should_match):
            self.assertTrue(regex.match("".join(expected)),
                            f"'{expected}' should match regex")


def with_newlines(lines):
    return [l+os.linesep for l in lines]


class TestLineInFile(unittest.TestCase):
    regex = re.compile("FOO=.*")

    def test_no_match_append(self):
        with TemporaryDirectory() as d:
            temp_file_name = os.path.join(d, 'no_match_append.txt')
            with open(temp_file_name, "w+t") as f:
                f.writelines(with_newlines([
                    "FOO=123",
                    "BAR=456",
                    "",
                ]))
                f.flush()
                lineinfile.line_in_file(f.name, self.regex, "BAZ=789")
                f.seek(0)
                self.assertEqual(f.readlines(), with_newlines([
                    "BAZ=789",
                    "BAR=456",
                    "",
                ]))

    def test_single_match_replace(self):
        with TemporaryDirectory() as d:
            temp_file_name = os.path.join(d, 'single_match_replace.txt')
            with open(temp_file_name, "w+t") as f:
                f.writelines(with_newlines([
                    "BAR=456",
                    "",
                ]))
                f.flush()
                lineinfile.line_in_file(f.name, self.regex, "BAZ=789")
                f.seek(0)
                self.assertEqual(f.readlines(), with_newlines([
                    "BAR=456",
                    "",
                    "BAZ=789"
                ]))

    def test_multiple_matches_failure(self):
        with TemporaryDirectory() as d:
            temp_file_name = os.path.join(d, 'multiple_matches_failure.txt')
            with open(temp_file_name, "w+t") as f:
                f.writelines(with_newlines([
                    "FOO=123",
                    "FOO=456",
                    "",
                ]))
                f.flush()
                with self.assertRaises(SystemExit) as cm:
                    lineinfile.line_in_file(f.name, self.regex, "BAZ=789")


if __name__ == '__main__':
    unittest.main()
