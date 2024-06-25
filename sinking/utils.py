import re
from typing import Optional


def create_pattern(name: str) -> Optional[str]:
    pattern = re.findall(r".*S\d\dE", name, flags=re.IGNORECASE)
    return pattern[0] if pattern else None
