import re
from pathlib import Path
import shutil
from src.errors import ShellError
from src.pathes import normalize_path, find_pathes

def cp(text: str) -> None:
    ''''''
    flag = None
    copying_path = None
    destination_path = None

    if text.startswith("-"):
        flag = text.split()[0][1::]
        text = re.sub(r"-[^\s]*", '', text, count=1)

    if not(flag == "r" or flag == None):
        raise ShellError(f"cp: invalid option -- '{flag.replace("r", "", 1)}'")
    
    if not text:
        raise ShellError("cp: missing file operand")
    else:
        pathes = find_pathes(text)

        if len(pathes) == 1:
            raise ShellError(f"cp: missing destination file operand after '{pathes[0]}'")
        elif len(pathes) > 2:
            raise ShellError(f"cp: too many arguments")
        
        copying_path = normalize_path(pathes[0])
        destination_path = normalize_path(pathes[1])
            
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

    # Если источник - директория
    # в линукс если дест не существует, то копирует именно содержимое директории,
    # без самой директории. Как бы копирует по существующему адресу и переименовывает
    # копи_паз в то, что написано в дист_паз
    if copying_path.is_dir():
        
        try:
            shutil.copytree(copying_path, destination_path, dirs_exist_ok=True)
        except PermissionError:
            raise ShellError(f"cp: permission denied: '{copying_path}'")
        except Exception as e:
            raise ShellError(f"cp: cannot copy directory '{copying_path}': {e}")
        # Нужно чтобы если дест дир существует, он НЕ затирал её, а просто копировал копи дир в неё
        # а если дест дир не существует, то создать такую же копию копи дир, но переименованную
    
    # Если источник - файл
    else:
        # Если цель - существующая директория, копируем файл в нее
        if destination_path.exists() and destination_path.is_dir():
            final_dest = destination_path / copying_path.name
        else:
            final_dest = destination_path
        
        try:
            '''
            # Создаем родительские директории, если нужно
            # линукс этого не делает
            if not final_dest.parent.exists():
                final_dest.parent.mkdir(parents=True)
            '''
            shutil.copy2(copying_path, final_dest)
        except PermissionError:
            print(f"cp: permission denied: '{copying_path}'")
        except Exception as e:
            print(f"cp: cannot copy '{copying_path}': {e}")