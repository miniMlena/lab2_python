import os
from pathlib import Path
from src.errors import ShellError
from src.paths import normalize_path, find_pathes

def cd(text: str) -> None:
    """
    Смены текущей директории на указанную
    :param text: Строка, содержащая путь, по которому нужно перейти (возможно пустая)
    :return: Данная функция ничего не возвращает
    """
    # Находим пути
    if not text:
        target_path = Path.home()
    else:
        pathes = find_pathes(text)
        if len(pathes) > 1:
            raise ShellError(f"cd: too many arguments")
        target_path = normalize_path(pathes[0])
    
    # Проверка ошибок
    if not target_path.exists():
        raise ShellError(f"cd: {target_path}: No such file or directory")
    
    if not target_path.is_dir():
        raise ShellError(f"cd: {pathes[0]}: Not a directory")
    
    try:
        os.chdir(target_path)
    except PermissionError:
        raise ShellError(f"cd: permission denied: {target_path}")
    except Exception as e:
        raise ShellError(f"cd: error changing directory: {e}")