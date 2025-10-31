import re
import shutil
from src.errors import ShellError
from src.paths import normalize_path, find_pathes

def cp(text: str) -> None:
    '''
    Копирование указанного файла по указанному пути.
    С опцией -r возможно рекурсивное копирование директорий
    :param text: Строка, содержащая опции, путь источника и путь назначения
    :return: Данная функция ничего не возвращает
    '''
    flag = None
    # Находим опции
    if text.startswith("-"):
        flag = text.split()[0][1::]
        text = re.sub(r"-[^\s]*", '', text, count=1)

    if not(flag == "r" or flag == None):
        raise ShellError(f"cp: invalid option -- '{flag.replace("r", "", 1)}'")
    
    if not text:
        raise ShellError("cp: missing file operand")
    
    # Находим пути
    pathes = find_pathes(text)

    if len(pathes) == 1:
        raise ShellError(f"cp: missing destination file operand after '{pathes[0]}'")
    elif len(pathes) > 2:
        raise ShellError(f"cp: too many arguments")
        
    copying_path = normalize_path(pathes[0])
    destination_path = normalize_path(pathes[1])
            
    # Проверка ошибок
    if not copying_path.exists():
        raise ShellError(f"cp: cannot stat '{copying_path}': No such file or directory")
    
    if copying_path.is_dir() and flag != "r":
        raise ShellError(f"cp: -r not specified; omitting directory '{pathes[0]}'")
    
    if not destination_path.parent.exists():
        raise ShellError(f"cp: cannot create {['regular file', 'directory'][copying_path.is_dir()]} '{destination_path}': No such file or directory")
    
    if copying_path.is_dir():
        if destination_path.exists() and not destination_path.is_dir():
            raise ShellError(f"cp: cannot overwrite non-directory '{pathes[1]}' with directory '{pathes[0]}'") 
        elif destination_path.is_dir():
            destination_path = destination_path / copying_path.name
        else:    # путь не существовал
            destination_path.mkdir()

    if copying_path.is_dir() and destination_path.is_relative_to(copying_path):
        raise ShellError(f"cp: cannot copy '{copying_path}' to a subdirectory of itself, '{destination_path}'")

    if copying_path.is_dir():
        try:
            shutil.copytree(copying_path, destination_path, dirs_exist_ok=True)
        except PermissionError:
            raise ShellError(f"cp: permission denied: '{pathes[0]}'")
        except Exception as e:
            raise ShellError(f"cp: cannot copy directory '{pathes[0]}': {e}")
    # Если источник - файл
    else:
        if destination_path.exists() and destination_path.is_dir():
            destination_path = destination_path / copying_path.name
        try:
            shutil.copy2(copying_path, destination_path)
        except PermissionError:
            raise ShellError(f"cp: permission denied: '{pathes[0]}'")
        except Exception as e:
            raise ShellError(f"cp: cannot copy '{pathes[0]}': {e}")