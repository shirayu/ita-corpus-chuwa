#!/usr/bin/env python3
import argparse
import difflib
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List

import jaconv


def add_temp_reading(path_in: Path, path_out_dir: Path):
    path_out = path_out_dir.joinpath(path_in.name)

    with path_in.open() as inf,\
            path_out.open('w') as outf:
        for line in inf:
            if line.startswith('# ') \
                    or line.startswith('@ ') \
                    or len(line) == 0\
                    or line == 'EOS\n':
                outf.write(line)
                continue
            else:
                line = line.strip()
                if line.endswith('NIL'):
                    line = line[:-3] + '"'
                elif line.endswith('"'):
                    line = line[:-1] + ' '
                    pass
                else:
                    raise NotImplementedError

                if line.startswith('は は は 助詞'):
                    r = 'ワ'
                else:
                    yomi: str = line.split()[1]
                    r = jaconv.hira2kata(yomi)

                outf.write(f'{line}発音:{r}"\n')


def check(path_in: Path,
          reading_info: Dict[str, List[str]],
          surf_info: Dict[str, List[str]],
          ) -> bool:
    err = False
    rs: List[str] = []
    surfs: List[str] = []
    with path_in.open() as inf:
        for line in inf:
            if '  ' in line:
                err = True
                print('There should not be double spaces')

            if line.startswith('# '):
                rs.append('')
                surfs.append('')
                continue

            if line.startswith('# ') \
                    or line.startswith('* ') \
                    or line.startswith('@ ') \
                    or line.startswith('+ ')\
                    or line == 'EOS\n':
                continue

            surfs[-1] += line.split()[0]
            if ' 未定義語 ' in line\
                    and not (
                        'ジャデャクシュ' in line
                        or 'ガリェント' in line
                        or 'ラーテャン' in line
                        or 'デョート' in line):
                print(f'未定義語: {line[:-1]}')
                err = True

            import csv
            import io
            r = None
            with io.StringIO() as f:
                f.write(line)
                f.seek(0)
                csv_reader = csv.reader(f, delimiter=' ')
                imis = [row for row in csv_reader][-1][-1]
                for imi in imis.split(' '):
                    if imi.startswith('発音:'):
                        r = imi[3:]
                        break
            if r is None:
                continue
            rs[-1] += r

    id: str = path_in.name.split('.')[0]
    reading = reading_info[id]
    gold_surfs = surf_info[id]

    if unicodedata.normalize('NFKC', ''.join(gold_surfs))\
            != unicodedata.normalize('NFKC', ''.join(surfs)):
        print(f'{gold_surfs}\n{surfs}')
        err = True

    for _r_gold, _r_sys in zip(reading, rs):
        _r_gold = _r_gold.rstrip('。').rstrip('？')
        if _r_gold != _r_sys:
            err = True
            print(id)
            print(_r_gold, _r_sys)
            d = difflib.Differ()
            diff = d.compare(_r_gold, _r_sys)
            out: str = ''
            for x in diff:
                if x.startswith(' '):
                    out += x.strip()
                else:
                    out += f'\n{x}\n'
            print(out.replace('\n\n', '\n'))
            print()

    return err


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--first", action="store_true")
    oparser.add_argument("--input", "-i", type=Path, required=True)
    oparser.add_argument("--output", "-o", type=Path, required=False)
    oparser.add_argument("--ref", "-r", action='append', type=Path)
    return oparser.parse_args()


def get_info(path_refs: List[Path], text: bool) -> Dict[str, List[str]]:
    ret: Dict[str, List[str]] = {}
    for path_r in path_refs:
        with path_r.open() as inf:
            for line in inf:
                id, scount, _text, _reading = line.strip().split('\t')
                if id not in ret:
                    ret[id] = []
                if text:
                    ret[id].append(_text)
                else:
                    ret[id].append(_reading)
    return ret


def main() -> None:
    opts = get_opts()
    err: bool = False

    for fpath in sorted(opts.input.iterdir()):
        if opts.first:
            opts.output.mkdir(exist_ok=True, parents=True)
            add_temp_reading(fpath, opts.output)
        else:
            readings = get_info(opts.ref, text=False)
            surfs = get_info(opts.ref, text=True)
            _err = check(fpath, readings, surfs)
            if _err:
                print(fpath)
            err |= _err

    if err:
        sys.exit(1)


if __name__ == '__main__':
    main()
