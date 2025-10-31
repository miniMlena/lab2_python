import re
import os
import shutil
from pathlib import Path
from src.errors import ShellError
from src.paths import normalize_path, find_pathes

def rm(text: str) -> None:
    '''
    Удаление указанного файла или директории
    :param text: Строка, содержащая путь к файлу или каталогу, который нужно удалить
    :return: Данная функция ничего не возвращает
    '''
    flag = None
    # Находим опции
    if text.startswith("-"):
        flag = text.split()[0][1::]
        text = re.sub(r"-[^\s]*", '', text, count=1)

    if not(flag == "r" or flag == None):
        raise ShellError(f"rm: invalid option -- '{flag.replace("r", "", 1)}'")
    
    if not text:
        raise ShellError("rm: missing operand")
    
    # Находим пути
    pathes = find_pathes(text)

    if len(pathes) > 1:
        raise ShellError(f"rm: too many arguments")
    
    removing_path = normalize_path(pathes[0])

    # Проверка ошибок
    if not removing_path.exists():
        raise ShellError(f"rm: cannot remove '{pathes[0]}': No such file or directory")
    
    if removing_path.is_dir() and flag != "r":
        raise ShellError(f"rm:  cannot remove '{pathes[0]}': Is a directory")
    
    if removing_path.parent == removing_path:
        raise ShellError(f"rm: cannot remove '{pathes[0]}': Root directory")
    
    if removing_path == Path.home():
        raise ShellError(f"rm: cannot remove '{pathes[0]}': Home directory")

    if removing_path.is_dir() and Path.cwd().is_relative_to(removing_path):
        raise ShellError(f"rm: cannot remove current working directory or its parent directories: '{removing_path}'")
    
    if removing_path.is_dir():
        response = input(f"rm: remove directory '{pathes[0]}' and all its contents? [y/n] ")
        if response.lower() in ['y', 'yes']:
            try:
                shutil.rmtree(removing_path)
            except PermissionError:
                raise ShellError(f"rm: cannot remove '{pathes[0]}': Permission denied")
            except Exception as e:
                raise ShellError(f"rm: cannot remove '{pathes[0]}': {e}")
    else:
        try:
            os.remove(removing_path)
        except PermissionError:
            raise ShellError(f"rm: cannot remove '{pathes[0]}': Permission denied")
        except Exception as e:
            raise ShellError(f"rm: cannot remove '{pathes[0]}': {e}")