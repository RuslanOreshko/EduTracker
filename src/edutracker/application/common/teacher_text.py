import re

def norm_name(s: str) -> str:
    return " ".join((s or "").lower().replace("’", "'").split())

def search_key(s: str) -> str:
    s = norm_name(s)
    s = s.replace(".", "")
    s = re.sub(r"\s+", "", s)
    return s

def split_teachers(raw: str) -> list[str]:
    if not raw:
        return []
    raw = raw.replace("/", " / ")
    parts = [p.strip() for p in raw.split(" / ")]
    return [p for p in parts if p]


def clean_display_name(name: str) -> str:
    if not name:
        return ""

    name = name.strip()
    name = name.strip("()")
    name = name.replace("’", "'")
    name = re.sub(r"\s+", " ", name)

    # прибрати крапку в кінці
    name = name.rstrip(".")

    return name.strip()