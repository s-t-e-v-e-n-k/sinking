import pathlib
import secrets
import string
import tempfile

from .options import Options
from .utils import create_pattern


class DestinationMatcher:
    def __init__(self) -> None:
        self.options = Options()
        self.destinations: dict[str, pathlib.Path] = {}
        self.walk()

    def walk(self) -> None:
        for path in self.options.destination.rglob("tmp.*/*"):
            if (p := create_pattern(path.parts[-1])) is not None:
                self.destinations[p] = path.parent

    def match(self, pattern: str) -> pathlib.Path:
        if pattern not in self.destinations:
            self.destinations[pattern] = self.new_dir()
        return self.destinations[pattern]

    def new_dir(self) -> pathlib.Path:
        alphabet = string.ascii_lowercase + string.digits + "_"
        if self.options.no_act:
            dir_part = "".join(secrets.choice(alphabet) for i in range(8))
            new_dir = self.options.destination / f"tmp.{dir_part}"
        else:
            tmp = tempfile.mkdtemp(
                prefix="tmp.", dir=self.options.destination
            )
            new_dir = pathlib.Path(tmp)
            new_dir.chmod(0o755)
        return new_dir
