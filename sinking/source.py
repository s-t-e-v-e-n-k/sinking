import dataclasses
import pathlib
import re
from typing import Optional

from .options import Options
from .utils import create_pattern


@dataclasses.dataclass
class SourceFile:
    path: pathlib.Path
    destination: Optional[pathlib.Path] = dataclasses.field(
        repr=False, default=None
    )

    @property
    def name(self) -> str:
        if self.needs_rename:
            return f"{self.path.parts[-2]}{self.path.suffix}"
        return self.path.name

    @property
    def pattern(self) -> Optional[str]:
        return create_pattern(self.name)

    @property
    def needs_rename(self) -> bool:
        return self.path.parts[-2][:6] != self.path.parts[-1][:6]

    @property
    def excluded(self) -> bool:
        o = Options()
        if re.search(r"sample", self.name, flags=re.IGNORECASE) is not None:
            return True
        if o.excludes:
            return any([True for e in o.excludes if e in self.name])
        if o.includes:
            return not any([True for i in o.includes if i in self.name])
        return False
