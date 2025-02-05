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

    def _randstr(self, length: int) -> str:
        alphabet = string.ascii_letters + string.digits + "_"
        return "".join(secrets.choice(alphabet) for i in range(length))

    def walk(self) -> None:
        for path in self.options.destination.rglob("tmp.*/*"):
            if (p := create_pattern(path.parts[-1])) != "":
                self.destinations[p] = path.parent

    def match(self, pattern: str) -> pathlib.Path:
        if pattern not in self.destinations:
            self.destinations[pattern] = self.new_dir()
        return self.destinations[pattern]

    def new_dir(self) -> pathlib.Path:
        meth = "fake_dir" if self.options.no_act else "real_dir"
        value: pathlib.Path = getattr(self, meth)()
        return value

    def fake_dir(self) -> pathlib.Path:
        dir_part = self._randstr(10)
        new_dir: pathlib.Path = self.options.destination / f"tmp.{dir_part}"
        return new_dir

    def real_dir(self) -> pathlib.Path:
        # mktempd doesn't match mktemp(1), add two characters as a suffix
        suffix = self._randstr(2)
        new_dir = pathlib.Path(
            tempfile.mkdtemp(
                suffix=suffix, prefix="tmp.", dir=self.options.destination
            )
        )
        new_dir.chmod(0o755)
        return new_dir
