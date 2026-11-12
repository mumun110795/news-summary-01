#!/usr/bin/env python3
"""news-summary-01 entry (Python 3.13, standard library only).

The repository holds the summary of Wednesday 11 November 2026 in
summary.txt, beside this file. The program writes it to entry.txt in
the output directory: /output in the grader's container, or the
directory named by MAKEFUN_OUTPUT_DIR when that is set.

The copy is byte-for-byte: the summary is read and written as raw
bytes, so no encoding or line-ending translation can alter it, and
every run produces identical output. Before writing, the program
checks the summary against the competition gate (UTF-8 text of 1 to
2,000 Unicode characters, not only whitespace) and fails loudly
instead of emitting an invalid entry.

The write itself is atomic: the bytes go to a temporary file in the
same directory, are flushed to disk, and are then moved over
entry.txt with os.replace, so an interrupted run can never leave a
truncated entry.txt behind. The temporary file is removed again if
anything fails before the move.
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 2000


def read_summary() -> bytes:
    """Return the raw bytes of summary.txt after validating them."""
    data = (Path(__file__).resolve().parent / "summary.txt").read_bytes()
    text = data.decode("utf-8")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"summary has {len(text)} characters, outside 1-{MAX_CHARS}")
    if not text.strip():
        raise ValueError("summary is only whitespace")
    return data


def write_entry(output_dir: Path, data: bytes) -> None:
    """Write data to entry.txt in output_dir, atomically."""
    target = output_dir / "entry.txt"
    temporary = output_dir / "entry.txt.tmp"
    try:
        with temporary.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    write_entry(output_dir, read_summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())
