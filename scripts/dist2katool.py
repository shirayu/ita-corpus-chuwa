#!/usr/bin/env python3
import argparse
import tarfile
import tempfile
from pathlib import Path


def work(path_in: Path, path_out: Path):
    path_out.parent.mkdir(exist_ok=True, parents=True)

    outs = []
    sids = []
    fileinfos = []
    with path_in.open() as inf:
        for line in inf:
            if line.startswith('# S-ID:'):
                outs.append('')
                sids.append(line[7:].split(' ')[0].strip())
                fileinfos.append(line)
                if 'MEMO:' not in line:
                    line = line.strip() + ' MEMO:\n'
            outs[-1] += line

    with tempfile.TemporaryDirectory() as tempdir:
        workdir = Path(tempdir).joinpath(path_in.stem)
        workdir.mkdir(exist_ok=True)

        with workdir.joinpath('fileinfos').open('w') as outf:
            outf.write(''.join(fileinfos))

        for sid, content in zip(sids, outs):
            with workdir.joinpath(sid).open('w') as outf:
                outf.write(content)

        with tarfile.open(path_out, mode='w:gz') as gzf:
            gzf.add(workdir, workdir.name)


def operation(path_in: Path, path_out_dir: Path) -> None:
    path_out_dir.mkdir(exist_ok=True, parents=True)
    for path_f in sorted(path_in.iterdir()):
        outname: Path = path_out_dir.joinpath(
            path_f.stem, f'{path_f.stem}.tar.gz')
        work(path_f, outname)


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, required=True)
    oparser.add_argument("--output", "-o", type=Path, required=True)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(opts.input, opts.output)


if __name__ == '__main__':
    main()
