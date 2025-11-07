import shutil
from pathlib import Path
from src.errors import ShellError
from src.paths import normalize_path, find_pathes
from src.undo_logging import log_move, remove_error_from_trash

def mv(text: str) -> None:
    '''
    Перемещение или переименование указанного файла или директории
    :param text: Строка, содержащая пути источника и назанчения
    :return: Данная функция ничего не возвращает
    '''
    if not text:
        raise ShellError("mv: missing file operand")
    
    # Находим пути
    pathes = find_pathes(text)

    if len(pathes) == 1:
        raise ShellError(f"mv: missing destination file operand after '{pathes[0]}'")
    elif len(pathes) > 2:
        raise ShellError(f"mv: too many arguments")
        
    moving_path = normalize_path(pathes[0])
    destination_path = normalize_path(pathes[1])
            
    # Проверка ошибок
    if not moving_path.exists():
        raise ShellError(f"mv: cannot stat '{moving_path}': No such file or directory")
    
    if moving_path == Path.cwd():
        raise ShellError(f"mv: cannot move current working directory: '{pathes[0]}'")

    if not destination_path.parent.exists():
        raise ShellError(f"mv: cannot move '{pathes[0]}' to '{pathes[1]}': No such file or directory")
    
    if moving_path == destination_path / moving_path.name:
        raise ShellError(f"mv: '{pathes[0]}' and '{moving_path}' are the same file")
    
    if moving_path.is_dir():
        if destination_path.exists() and not destination_path.is_dir():
            raise ShellError(f"mv: cannot overwrite non-directory '{pathes[1]}' with directory '{pathes[0]}'")

    if moving_path.is_dir() and destination_path.is_relative_to(moving_path):
        raise ShellError(f"mv: cannot move '{moving_path}' to a subdirectory of itself, '{destination_path}'")

    if destination_path.exists() and destination_path.is_dir():
        destination_path = destination_path / moving_path.name
    
    try:
        # Сначала логируем, иначе потом необохдимая информация уже будет удалена
        log_move(moving_path, destination_path)
        shutil.move(str(moving_path), str(destination_path))
    except PermissionError:
        # Стираем из .trash лог об ошибочной операции
        remove_error_from_trash()
        raise ShellError(f"mv: cannot move '{pathes[0]}': Permission denied")
    except Exception as e:
        remove_error_from_trash()
        raise ShellError(f"mv: cannot move '{pathes[0]}': {e}")
