#!/usr/bin/python3

"""
This script searches a value in a file. If found it will be replaced.
If not found, the replacement value is appended to the file.
Similar to Ansible's lineinfile without requiring ansible and with
verbose output.
"""

import re
import sys
from collections import namedtuple


def get_regex(find: str) -> re.Pattern:
    return re.compile(r"(\s*)(#|//)?(\s*)"+find+r".*")


Match = namedtuple('Match', ['index', 'value'])


def line_in_file(filename: str, find_regex: re.Pattern, replace: str):
    # Read file
    with open(filename, 'rt') as f:
        lines = f.readlines()

    # Search for matches
    matches: list[Match] = []
    for i, line in enumerate(lines):
        match = find_regex.match(line)
        if match:
            matches.append(Match(i, match[0]))

    # Process matches
    replace_with_newline = replace+"\n"
    matches_len = len(matches)
    if matches_len == 0:
        print(
            f"No match found in file '{filename}'. Appending '{replace}' to end ...")
        with open(filename, 'at') as f:
            f.write(replace_with_newline)
    elif matches_len == 1:
        match = matches[0]
        if match.value == replace:
            print(
                f"Found match on line {match.index+1} in file '{filename}': '{match.value}'. Value already the same as replacement value.")
        else:
            print(
                f"Found match on line {match.index+1} in file '{filename}': '{match.value}'. Replacing with '{replace}'.")
            lines[match.index] = replace_with_newline
            with open(filename, 'wt') as f:
                f.writelines(lines)
    else:
        print(f"ERROR: Found multiple matches in file '{filename}':")
        for match in matches:
            print(f"- {match.index+1}: '{match.value}'")
        sys.exit(1)


def main():
    # Parse args
    if len(sys.argv) != 4:
        sys.exit("Expects exactly 3 params")  # 4th param is script call
    [_, filename, find, replace] = sys.argv

    # Update file
    find_regex = get_regex(find)
    line_in_file(filename, find_regex, replace)


if __name__ == '__main__':
    main()
