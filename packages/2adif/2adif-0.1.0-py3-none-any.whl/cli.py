import argparse
from pathlib import Path

from main import TO_ADIF


def _do(path: Path):
    to_adif = TO_ADIF(path)
    # to_adif.get_adif_str()
    to_adif.to_adif(path.with_suffix(path.suffix + ".adi"))


class Args(argparse.Namespace):
    path: list[Path]


def cli():
    parser = argparse.ArgumentParser(prog="2adif")

    parser.add_argument(
        "path",
        nargs="+",
        type=Path,
        help="the .csv file(s) that you want to convert to .adi",
    )

    args: Args = parser.parse_args(namespace=Args())

    print()
    print("====== 2adif cli ======")
    print(args)

    paths: list[Path] = []
    EXT = ".csv"
    for path in args.path:
        if path.suffix == EXT:
            paths.append(path)
        elif path.is_dir():
            for child_path in path.iterdir():
                if child_path.suffix == EXT:
                    paths.append(child_path)

    for path in paths:
        print()
        print("[cli.py]", "processing:", path)
        _do(path)

    print()
    print("[cli.py]", "processed files:", len(paths))


if __name__ == "__main__":
    cli()
    print()
