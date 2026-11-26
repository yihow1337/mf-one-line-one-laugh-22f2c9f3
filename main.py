#!/usr/bin/env python3
"""Write the competition artifact: one funny line, at most 200 characters.

Three steps, one function each: read the authored line from entry.txt beside
this script, check it against every condition the sealed gate applies, then
write it to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt). The line is
the whole entry, so the artifact is the bare text with no trailing newline.

Nothing here consults a clock, a random source or the network, and the only
input is a file committed next to it, so every run writes identical bytes.
Standard library only.
"""

import os
import sys

# Where the line is authored, and where the judge expects to find it.
SOURCE_FILE = "entry.txt"
ARTIFACT_NAME = "entry.txt"
OUTPUT_DIR_ENV = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"

# The sealed scorer's limit: UTF-8 text of 1 to 200 characters, not only space.
MAX_CHARS = 200


def read_line() -> str:
    """Return the authored line, stripped to exactly the text of the joke.

    .strip() removes the file's trailing newline along with any stray spaces,
    so the artifact is the bare line: no padding to inflate the byte count,
    which the leaderboard uses as a tie-break in favour of smaller texts.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, SOURCE_FILE), encoding="utf-8") as f:
        return f.read().strip()


def check_gate(line: str) -> str:
    """Return "" if the line passes the gate, else why it would be refused.

    Every condition the sealed scorer applies, stated once, in one place.
    """
    if not line.strip():
        return "entry is empty or only white space"
    if len(line) > MAX_CHARS:
        return "entry is %d characters, over the %d limit" % (len(line), MAX_CHARS)
    if "\n" in line or "\r" in line:
        return "entry must be a single line"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not encodable as UTF-8"
    return ""


def write_artifact(line: str) -> str:
    """Write the line to the output directory and return the path written.

    newline="" keeps write() from translating anything on the way out, so the
    bytes on disk are exactly the bytes of the line on every platform.
    """
    out_dir = os.environ.get(OUTPUT_DIR_ENV) or DEFAULT_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, ARTIFACT_NAME)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    return out_path


def main() -> int:
    line = read_line()

    refusal = check_gate(line)
    if refusal:
        print(refusal, file=sys.stderr)
        return 1

    out_path = write_artifact(line)
    print("wrote %s (%d characters, %d bytes)" % (out_path, len(line), len(line.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
