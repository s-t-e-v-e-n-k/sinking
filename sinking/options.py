from __future__ import annotations

from types import SimpleNamespace
from typing import ClassVar


class Options(SimpleNamespace):
    instance: ClassVar[Options]

    def __new__(cls) -> Options:
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    @classmethod
    def clear(cls) -> None:
        if hasattr(cls, "instance"):
            del cls.instance
