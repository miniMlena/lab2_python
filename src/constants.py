import re
from pathlib import Path

# Паттерн для поиска путей в строке
PATH_RE: re.Pattern = re.compile(
    r"""
    (?:[^\s"]*\\?["][^\\"]*\s+[^\\"]*["]\\?[^\s"]*)+
    |[^\s]+
    """,
    re.VERBOSE
)

# Путь к файлу .trash. Указан явно, чтобы не возникало ошибок независимо от того,
# в какой директории находится пользователь. При этом не зависит от директории, из которой запускается программа
trash_file: Path = Path(__file__).resolve().parent.parent / '.trash'

# Аналогичный путь к файлу .history
history_file: Path = Path(__file__).resolve().parent.parent / '.history'