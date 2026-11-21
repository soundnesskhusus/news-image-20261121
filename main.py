#!/usr/bin/env python3
"""news-image-20261121 entry: write the 21 November 2026 front page to
/output/entry.png.

The front page is bundled beside this file (entry.png, drawn in-session
for this entry with Pillow). The program only copies it: no network, no
randomness, so two runs write identical bytes. Outside the grader,
MAKEFUN_OUTPUT_DIR stands in for /output.
"""
import hashlib
import os
import shutil
import struct

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"IEND"

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(DST_DIR, "entry.png")


def check_output(path):
    """Refuse to finish with a broken file: PNG magic, 1024x1024, <= 1 MiB."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit("entry.png is %dx%d, expected 1024x1024"
                         % (width, height))
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB cap"
                         % len(data))

    # The gate wants a whole image, so confirm the IEND chunk is present:
    # the last 12 bytes are its length (0), type, and CRC.
    if data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != PNG_IEND:
        raise SystemExit("entry.png is missing its IEND chunk")
    print("entry.png OK: 1024x1024, %d bytes, sha256 %s"
          % (len(data), hashlib.sha256(data).hexdigest()[:12]))


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    check_output(DST)


if __name__ == "__main__":
    main()
