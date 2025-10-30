from src.constants import COMMAND_RE
from src.ls import ls
from src.cd import cd
from src.cat import cat
from src.cp import cp
from src.mv import mv
from src.errors import ShellError

def execute(text: str) -> None:
    text = text.strip()
    if text:
        if text.startswith("ls"):
            ls(text[2::].strip())
        elif text.startswith("cd"):
            cd(text[2::].strip())
        elif text.startswith("cat"):
            cat(text[3::].strip())
        elif text.startswith("cp"):
            cp(text[2::].strip())
        elif text.startswith("mv"):
            mv(text[2::].strip())

        else:
            raise ShellError(f"{text.split(maxsplit = 1)[0]}: command not found")