import re


def create_pattern(name: str) -> str:
    pattern: list[str] = re.findall(r".*S\d\dE", name, flags=re.IGNORECASE)
    return pattern[0] if pattern else ""
