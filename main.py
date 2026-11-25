#!/usr/bin/env python3
"""Write the one word from my ex to /output/entry.txt.

A single word, frozen in the source code. The script accepts no
input and leans on no network, no clock and no randomness, so the
bytes it writes are the same on the first run and the hundredth.
"""

import sys
from pathlib import Path

ENTRY = "Forgettable"
CHAR_LIMIT = 24
DEST = Path("/output/entry.txt")


class RejectedEntry(ValueError):
    """The frozen word failed a check."""


def inspect_entry(word):
    """Inspect the word, size checks before character checks."""
    if word is None or word.strip() == "":
        raise RejectedEntry("entry is empty or whitespace only")
    if len(word) > CHAR_LIMIT:
        raise RejectedEntry("entry exceeds the 24-character limit")
    if " " in word:
        raise RejectedEntry("entry must be one word with no space")
    if word.startswith("-") or word.endswith("-"):
        raise RejectedEntry("entry must not start or end with a hyphen")
    if any(ord(ch) < 32 for ch in word):
        raise RejectedEntry("entry contains a control character")
    if word != word.strip():
        raise RejectedEntry("entry has a leading or trailing space")
    if any(ch.isdigit() for ch in word):
        raise RejectedEntry("entry contains a digit")
    if word.isdigit():
        raise RejectedEntry("entry is digits only")
    if not any(ch.isalpha() for ch in word):
        raise RejectedEntry("entry has no letter at all")
    return word


def main():
    """Inspect the frozen word and write it to the output path."""
    try:
        cleared = inspect_entry(ENTRY)
    except RejectedEntry as err:
        print(f"entry rejected: {err}", file=sys.stderr)
        return 1
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(cleared, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
