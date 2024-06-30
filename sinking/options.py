from types import SimpleNamespace


class Options(SimpleNamespace):
    def __new__(cls) -> "Options":
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    @classmethod
    def clear(cls) -> None:
        if hasattr(cls, "instance"):
            del cls.instance
