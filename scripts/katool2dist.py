#!/usr/bin/env python3

import argparse
import csv
import io
import tarfile
from pathlib import Path


def trim_conent(data: str) -> str:
    # Currently ignore rels

    def _is_eos(line: str) -> bool:
        return line == 'EOS' \
            or line == 'EOS\n' \
            or len(line) == 0

    def _is_special_line(line: str) -> bool:
        return line.startswith('# ') \
            or line.startswith('* ') \
            or line.startswith('+ ')

    output = io.StringIO()
    writer = csv.writer(output, delimiter=" ", lineterminator='\n')
    for line in data.split('\n'):
        if len(line) == 0:
            continue
        elif line.startswith('@'):
            raise NotImplementedError
        elif _is_eos(line):
            writer.writerow([line.strip()])
        elif _is_special_line(line):
            items = next(csv.reader([line], delimiter=' '))
            writer.writerow(items[:2])
        else:
            items = next(csv.reader([line], delimiter=' '))
            writer.writerow(items[:12])
    return output.getvalue()


def extract_for_document(path_input: Path) -> str:
    sid2content = {}
    sids = []
    with tarfile.open(path_input, 'r') as tarf:
        for member in tarf.getmembers():
            if member.isdir():
                continue
            mi = tarf.extractfile(member)
            assert mi is not None
            mydata = mi.read().decode('utf8')
            if member.name.endswith('fileinfos'):
                for line in mydata.split('\n'):
                    if len(line) > 0:
                        sids.append(line.split()[1][5:])
            else:
                sid2content[Path(member.name).name] = trim_conent(mydata)

    return ''.join([sid2content[sid] for sid in sids])


def operation(path_in: Path, path_out: Path) -> None:
    path_out.mkdir(exist_ok=True, parents=True)
    for inpath in sorted(path_in.glob('**/*.tar.gz')):
        if len(inpath.name.split('.')) != 3:
            continue
        with path_out.joinpath(f'{inpath.name.split(".")[0]}.knp')\
                .open('w') as outf:
            outf.write(extract_for_document(inpath))


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
