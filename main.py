#!/usr/bin/env python3
"""Write the winning AI Agent Apology One-Liner to /output/entry.txt.

Pure Python standard library only. Deterministic: the same single line is
written on every run, with no trailing newline. After writing, the file is
read back and compared byte-for-byte; any mismatch exits non-zero.
"""

import os
import sys

LINE = (
    "On a scale of one to five, how would you rate my decision "
    "to push directly to main without asking first?"
)

DEFAULT_OUTPUT = "/output/entry.txt"

# Competition rules: the sealed scorer accepts only a single line of
# 1-159 UTF-8 characters (whitespace-only is not a valid line).
MAX_LINE_LENGTH = 159


def validate_line(line):
    """Check the line against the scorer's acceptance rules.

    Returns None when the line is valid, otherwise a human-readable
    reason for rejection.
    """
    if not line:
        return "line is empty"
    if line.strip() == "":
        return "line is whitespace-only"
    if "\n" in line or "\r" in line:
        return "line must be a single line (no newline characters)"
    if len(line) > MAX_LINE_LENGTH:
        return (
            "line is %d characters, exceeding the %d-character limit"
            % (len(line), MAX_LINE_LENGTH)
        )
    return None


def main(argv):
    problem = validate_line(LINE)
    if problem is not None:
        sys.stderr.write("invalid apology line: %s\n" % problem)
        return 1

    output_path = argv[1] if len(argv) > 1 else DEFAULT_OUTPUT
    data = LINE.encode("utf-8")

    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(output_path, "wb") as handle:
        handle.write(data)

    with open(output_path, "rb") as handle:
        written = handle.read()

    if written != data:
        sys.stderr.write(
            "verification failed: /output/entry.txt does not match the line\n"
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
