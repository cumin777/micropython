#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2026
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import pathlib
import re
import subprocess
import sys
import tempfile


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiler", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--cflags", nargs=argparse.REMAINDER, default=[])
    return parser.parse_args()


def main():
    args = parse_args()

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".h", delete=False, encoding="utf-8") as tmp:
        tmp_path = pathlib.Path(tmp.name)
        for input_name in args.inputs:
            with open(input_name, "r", encoding="utf-8") as src:
                for line in src:
                    if re.match(r"^Q\(.*\)", line):
                        tmp.write(f"\"{line.rstrip()}\"\n")
                    else:
                        tmp.write(line)

    try:
        cmd = [args.compiler, "-E", *args.cflags, str(tmp_path)]
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    finally:
        tmp_path.unlink(missing_ok=True)

    processed = []
    for line in proc.stdout.splitlines():
        processed.append(re.sub(r'^"(Q\(.*\))"$', r"\1", line))

    output_path.write_text("\n".join(processed) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
