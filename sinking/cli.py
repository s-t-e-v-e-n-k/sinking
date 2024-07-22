import argparse
import logging
import pathlib
import shutil
import sys

if sys.version_info >= (3, 9):  # pragma: no cover
    from collections.abc import Generator
else:  # pragma: no cover
    from typing import Generator

from . import __version__
from .destination import DestinationMatcher
from .options import Options
from .source import SourceFile


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"sinking {__version__}"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-e",
        "--excludes",
        action="append",
        default=[],
        help="exclude things that match",
    )
    group.add_argument(
        "-i",
        "--includes",
        action="append",
        default=[],
        help="include things that match",
    )
    parser.add_argument(
        "-n",
        "--no-act",
        action="store_true",
        help="do not perform any actions",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        action="store",
        default="*.mkv",
        help="pattern to match on (default: *.mkv)",
    )
    parser.add_argument(
        "-s",
        "--source",
        default="/srv/podman",
        type=pathlib.Path,
        help="source directory (default: /srv/podman)",
    )
    parser.add_argument(
        "-d",
        "--destination",
        default="/srv/media/.incoming",
        type=pathlib.Path,
        help="destination directory (default: /srv/media/.incoming)",
    )
    parser.add_argument(
        "-r",
        "--rename",
        action="store_false",
        default=True,
        help="do not rename files to match directory name",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="show debug messages",
    )
    return parser


class Copier:
    def __init__(self) -> None:
        self.options = Options()
        self.dm = DestinationMatcher()

    @property
    def sources(self) -> Generator[SourceFile, None, None]:
        for path in self.options.source.rglob(self.options.pattern):
            logging.debug(f"Considering {path}")
            s = SourceFile(path)
            if s.excluded:
                logging.debug("\tExcluded")
                continue
            s.destination = self.dm.match(s.pattern)
            if (s.destination / s.name).exists():
                logging.debug(f"{s.name} already exists")
                continue
            logging.debug(
                f"Setting destination of {s.name} to {s.destination}"
            )
            yield s

    def copy(self) -> None:
        sources = list(self.sources)
        for count, source in enumerate(sources, start=1):
            logging.info(
                f"{source.name} -> {source.destination.name} "
                f"[{count}/{len(sources)}]"
            )
            if not self.options.no_act:
                shutil.copy(source.path, source.destination / source.name)


def main() -> int:
    args = parser().parse_args()
    options = Options()
    for key in args.__dict__:
        setattr(options, key, getattr(args, key))
    level = logging.DEBUG if options.verbose else logging.INFO
    logging.basicConfig(format="%(message)s", level=level)
    c = Copier()
    c.copy()
    return 0
