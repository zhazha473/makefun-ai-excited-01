"""make.fun ai-excited-01 entry.

A glowing golden koi leaps diagonally out of a dark midnight ocean
into a swirling aurora sky, its spray of water droplets turning into
stars mid-flight. The twist is the impossible scale jump: a fish
leaving the sea for the sky, so the splash itself becomes starlight.

The program below is a deterministic copier: it reads entry.png from
this directory and writes an identical copy to the output directory
as entry.png. No network, no randomness, no clock, no image
re-encoding — the output bytes are exactly the input bytes, so two
runs always produce the same sha256.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_png_dimensions(data: bytes) -> tuple[int, int]:
    """Return (width, height) parsed from a PNG IHDR chunk."""
    if len(data) < 24 or data[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png is not a valid PNG file")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    data = source.read_bytes()
    if len(data) > MAX_BYTES:
        print(
            f"error: {SOURCE_NAME} is {len(data)} bytes, over the "
            f"{MAX_BYTES} byte limit",
            file=sys.stderr,
        )
        return 1
    width, height = read_png_dimensions(data)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        print(
            f"error: {SOURCE_NAME} is {width}x{height}, over the "
            f"{MAX_DIMENSION}x{MAX_DIMENSION} limit",
            file=sys.stderr,
        )
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / OUTPUT_NAME
    shutil.copyfile(source, dest)

    copied = dest.read_bytes()
    if copied != data:
        print("self-check FAILED: output bytes differ from source", file=sys.stderr)
        return 1

    print(f"wrote {len(copied)} bytes ({width}x{height}) to {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
