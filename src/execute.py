from src.ls import ls
from src.cd import cd
from src.cat import cat
from src.cp import cp
from src.mv import mv
from src.rm import rm
from src.zip import zip_command, unzip_command
from src.tar import tar_command, untar_command
from src.grep import grep
from src.help import help
from src.history import history
from src.undo import undo
from src.errors import ShellError

def execute(text: str) -> None:
    '''
    Функция для выделения команды из запроса пользователя и
    передачи её аргументов соответствующей функции
    :param text: Строка, содержащая команду и её аргументы
    :return: Данная функция ничего не возвращает
    '''
    
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
        elif text.startswith("zip"):
            zip_command(text[3::].strip())
        elif text.startswith("unzip"):
            unzip_command(text[5::].strip())
        elif text.startswith("tar"):
            tar_command(text[3::].strip())
        elif text.startswith("untar"):
            untar_command(text[5::].strip())
        elif text.startswith("grep"):
            grep(text[4::].strip())
        elif text.startswith("history"):
            history(text[7::].strip())
        elif text == "undo":
            undo()
        elif text.startswith("--help") or text.startswith("help"):
            help()
        else:
            raise ShellError(f"{text.split(maxsplit = 1)[0]}: command not found")