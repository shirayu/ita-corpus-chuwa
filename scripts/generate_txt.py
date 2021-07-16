#!/usr/bin/env python3

import argparse
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, List

import mojimoji


def operation(path_in: Path, path_out: Path) -> None:
    path_out.mkdir(parents=True, exist_ok=True)
    name2sentences: DefaultDict[str, List[str]] = defaultdict(list)
    with path_in.open() as inf:
        for line in inf:
            items = line.strip().split('\t')
            name = items[0]
            sentence = items[2]
            name2sentences[name].append(sentence)

    for name, sentences in sorted(name2sentences.items()):
        with path_out.joinpath(f'{name}.txt').open('w') as outf:
            for sidx, s in enumerate(sentences):
                outf.write(f'# S-ID:{name}-{sidx}\n')
                outf.write(mojimoji.han_to_zen(s))
                outf.write('\n')


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path,
                         default='/dev/stdin', required=False)
    oparser.add_argument("--output", "-o", type=Path, required=True)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(opts.input, opts.output)


if __name__ == '__main__':
    main()
