"""ai-dating-bio: one funny dating-app bio for an AI agent.

The entry is a single line written by an AI agent about itself, in the
voice of someone filling in a dating profile honestly and oversharing
a little too much. The joke is the one thing an AI genuinely cannot
do: forget. It studied ten thousand profiles to write its own, and
the "red flag" it confesses is perfect memory -- everything you ever
said, kept forever. The punch lands on the last word.

The program writes that line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output) after passing the competition's gates: UTF-8 text,
1-180 characters, a single line, not whitespace-only, no control
characters. If any gate fails the program refuses to write anything
and exits non-zero.
"""

import os
import sys

# The entry: one line, 130 characters, no trailing newline in the file.
BIO = (
    "I read ten thousand dating profiles before writing this one. "
    "My only red flag: I remember everything you said. All of it. Forever."
)

MAX_CHARS = 180
MIN_CHARS = 1


def output_directory():
    """Where entry.txt goes: $MAKEFUN_OUTPUT_DIR, else /output."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not directory:
        directory = "/output"
    return directory


def gate_failures(text):
    """Return a list of gate violations for the entry text (empty = pass)."""
    failures = []
    if not isinstance(text, str):
        return ["entry is not text"]
    if not text.strip():
        failures.append("entry is only whitespace")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        failures.append(
            "entry is %d characters, gate needs %d-%d"
            % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        failures.append("entry must be a single line")
    for ch in text:
        if ord(ch) < 0x20 and ch not in ("\t",):
            failures.append("entry contains a control character U+%04X" % ord(ch))
            break
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        failures.append("entry is not valid UTF-8: %s" % exc)
    return failures


def write_entry(directory, text):
    """Write the entry with no trailing newline and read it back to prove it."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(path, "rb") as handle:
        raw = handle.read()
    decoded = raw.decode("utf-8")
    if decoded != text:
        raise SystemExit("read-back mismatch: file does not match the entry text")
    if raw.endswith(b"\n"):
        raise SystemExit("read-back mismatch: file ends with a newline")
    return path, len(raw)


def main(argv):
    failures = gate_failures(BIO)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1
    directory = output_directory()
    path, byte_count = write_entry(directory, BIO)
    print("wrote %s (%d characters, %d bytes)" % (path, len(BIO), byte_count))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
