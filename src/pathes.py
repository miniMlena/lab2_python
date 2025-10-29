from pathlib import Path
from src.constants import PATH_RE

def find_pathes(text: str) -> list:
    text = text.strip()
    return PATH_RE.findall(text)

def normalize_path(path: str) -> Path:
    ''''''
    path = path.replace('"', '')

    if path == "~":
        path = Path.home()
    elif path == ".":
        path = Path.cwd()
    elif path == "..":
        path = Path.cwd().parent
    elif path.startswith("~/") or path.startswith("~\\"):
        path = Path.home() / path[2:]
    else:
        path = Path(path)
        if not path.is_absolute():
            path = Path.cwd() / path

    return path