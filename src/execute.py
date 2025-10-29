from src.constants import COMMAND_RE
from src.ls import ls
from src.cd import cd
from src.errors import ShellError

def execute(text: str) -> None:
    text = text.strip()
    if text:
        if text.startswith("ls"):
            ls(text[2::].strip())
        elif text.startswith("cd"):
            cd(text[2::].strip())
            
        else:
            raise ShellError(f"{text.split(maxsplit = 1)[0]}: command not found")