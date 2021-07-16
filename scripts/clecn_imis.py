#!/usr/bin/env python3

import argparse
import csv
import io
from pathlib import Path


def get(line):
    with io.StringIO() as f:
        f.write(line)
        f.seek(0)
        csv_reader = csv.reader(f, delimiter=' ')
        info = [row for row in csv_reader][-1]
        x = []
        for imi in info[-1].split(' '):
            if imi.startswith('発音:'):
                x.append(imi)
            elif imi.startswith('代表表記:'):
                x.append(imi)
            elif imi.startswith('疑似代表表記'):
                x.append(imi)
        if len(x) >= 2:
            info[-1] = '"' + ' '.join(sorted(x)) + '"'
        else:
            info[-1] = x[0]
    return ' '.join(info)


def operation(path_in: Path, path_out: Path) -> None:
    with path_in.open() as inf,\
            path_out.open('w') as outf:
        for line in inf:
            if '発音' in line:
                line = get(line) + '\n'
            outf.write(line)


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
