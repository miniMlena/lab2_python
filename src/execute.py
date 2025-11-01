from src.constants import COMMAND_RE
from src.ls import ls
from src.cd import cd
from src.cat import cat
from src.cp import cp
from src.mv import mv
from src.rm import rm
from src.grep import grep
from src.help import help
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
        elif text.startswith("rm"):
            rm(text[2::].strip())
        elif text.startswith("grep"):
            grep(text[4::].strip())
        elif text.startswith("--help") or text.startswith("help"):
            help()
        else:
            raise ShellError(f"{text.split(maxsplit = 1)[0]}: command not found")