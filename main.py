#!/usr/bin/env python3
"""Write the competition artifact: one funny line, at most 200 characters.

The line itself lives in entry.txt next to this script. We read it, strip the
trailing newline so the artifact is exactly the line and nothing else, and
write it to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt). No clocks, no
randomness, no network: identical bytes on every run.
"""

import os
import sys

MAX_CHARS = 200


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.txt"), encoding="utf-8") as f:
        line = f.read()

    # The artifact is the bare line: no trailing newline, no surrounding space.
    line = line.strip("\r\n").strip()

    if not line or line.isspace():
        print("entry.txt is empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print("entry is %d characters, over the %d limit" % (len(line), MAX_CHARS), file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("entry must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)

    print("wrote %s (%d characters, %d bytes)" % (out_path, len(line), len(line.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
