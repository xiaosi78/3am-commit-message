"""Write one funny 3 AM commit message to /output/entry.txt.

Deterministic: the same single line is written on every run, with no
trailing newline, so the sealed scorer sees exactly 1-200 characters.
"""

import os

LINE = "fix: broke prod at 3 AM, asked myself for a code review and I approved it"

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    if not 1 <= len(LINE) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(LINE)}")
    if not LINE.strip():
        raise ValueError("entry must not be only whitespace")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Verify the bytes on disk are exactly the intended line, and that
    # the entry still satisfies the 1-200 character gate.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        raise RuntimeError(
            f"read-back mismatch: wrote {len(LINE.encode('utf-8'))} bytes, "
            f"read back {len(written)} bytes"
        )
    if not 1 <= len(written.decode("utf-8")) <= 200:
        raise ValueError(
            f"entry must be 1-200 characters, got {len(written.decode('utf-8'))}"
        )


if __name__ == "__main__":
    main()
