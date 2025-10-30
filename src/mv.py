import os
import shutil
from src.errors import ShellError
from src.pathes import normalize_path, find_pathes

def mv(text: str) -> None:
    ''''''
    moving_path = None
    destination_path = None
    
    if not text:
        raise ShellError("mv: missing file operand")
    else:
        pathes = find_pathes(text)

        if len(pathes) == 1:
            raise ShellError(f"mv: missing destination file operand after '{pathes[0]}'")
        elif len(pathes) > 2:
            raise ShellError(f"mv: too many arguments")
        
        moving_path = normalize_path(pathes[0])
        destination_path = normalize_path(pathes[1])
            
    if not moving_path.exists():
        raise ShellError(f"mv: cannot stat '{moving_path}': No such file or directory")
    
    if not os.access(moving_path, os.R_OK):
        raise ShellError(f"mv: cannot move '{moving_path}': Permission denied")

    if not destination_path.parent.exists():
        raise ShellError(f"mv: cannot move '{pathes[0]}' to '{pathes[1]}': No such file or directory")
    
    if moving_path == destination_path / moving_path.name:
        raise ShellError(f"mv: '{pathes[0]}' and '{moving_path}' are the same file")
    '''
    if moving_path.is_dir():
        if destination_path.exists() and not destination_path.is_dir():
            raise ShellError(f"mv: cannot overwrite non-directory '{pathes[1]}' with directory '{pathes[0]}'") 
        elif destination_path.is_dir():
            destination_path = destination_path / moving_path.name #переместить ДИРЕКТОРИЮ по этому пути
        else:    # путь не существовал
            destination_path.mkdir() # и в него переместить СОДЕРЖИМОЕ мувинга
    '''
    '''
    if not moving_path.is_dir():
        if destination_path.exists():
            moving_path = moving_path # мб с перезаписью
        else:
            # воспринимать последнее слвоо в пути как новое имя файла
            # с файлами кажись нет такой фигни
            '''

    if moving_path.is_dir() and destination_path.is_relative_to(moving_path):
        raise ShellError(f"mv: cannot move '{moving_path}' to a subdirectory of itself, '{destination_path}'")

    if moving_path == destination_path / moving_path.name:
        print("*")
        raise ShellError(f"mv: '{moving_path}' and '{pathes[1]}/{moving_path.name}' are the same file")

    if destination_path.exists() and destination_path.is_dir():
        destination_path = destination_path / moving_path.name
    
    try:
        shutil.move(str(moving_path), str(destination_path))
    #except PermissionError:
    #    print(f"*mv: cannot move '{moving_path}': Permission denied")
    except FileExistsError:
        (f"mv: '{pathes[0]}' and '{destination_path}' are the same file")
    except Exception as e:
        print(f"mv: cannot move '{moving_path}': {e}")
