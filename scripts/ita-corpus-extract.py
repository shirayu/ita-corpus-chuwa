#!/usr/bin/env python3

import argparse
import re
from pathlib import Path

SBD = re.compile(r"(?<=[。？！?!])")


def operation(path_in: Path, path_out: Path) -> None:
    with path_in.open() as inf,\
            path_out.open('w') as outf:
        for line in inf:
            assert '\t' not in line
            name, content = line.strip().split(':', 1)
            sentences, readings = content.split(',', 1)

            for idx, (sentence, reading) in \
                    enumerate(zip(SBD.split(sentences), SBD.split(readings))):
                if len(sentence) == 0:
                    break
                outf.write(f'{name}\t{idx}\t{sentence}\t{reading}\n')


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path,
                         default='/dev/stdin', required=False)
    oparser.add_argument("--output", "-o", type=Path,
                         default="/dev/stdout", required=False)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(opts.input, opts.output)


if __name__ == '__main__':
    main()
