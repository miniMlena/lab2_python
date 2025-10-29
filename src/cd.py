import os
from pathlib import Path
from src.errors import ShellError
from src.pathes import normalize_path, find_pathes

def cd(text: str | None):
    """
    Реализация команды cd для смены текущей рабочей директории
    Использование: cd [path] или cd ~ или cd ..
    """
    if not text:
        target_path = Path.home()
    else:
        pathes = find_pathes(text)
        if len(pathes) > 1:
            raise ShellError(f"cd: too many arguments")
        target_path = normalize_path(pathes[0])
    
    if not target_path.exists():
        raise ShellError(f"cd: {target_path}: No such file or directory")
    
    if not target_path.is_dir():
        raise ShellError(f"cd: {target_path}: Not a directory")
    
    try:
        os.chdir(target_path)
    except PermissionError:
        raise ShellError(f"cd: permission denied: {target_path}")
    except Exception as e:
        raise ShellError(f"cd: error changing directory: {e}")


'''
# Альтернативная более простая версия с использованием os.path
def cd_simple(args=None):
    """
    Упрощенная версия команды cd с использованием os.path
    """
    if not args:
        # Переход в домашний каталог
        home_dir = os.path.expanduser("~")
        os.chdir(home_dir)
        return
    
    path_arg = args[0]
    
    # Обработка специальных случаев
    if path_arg == "~":
        home_dir = os.path.expanduser("~")
        os.chdir(home_dir)
    elif path_arg == "..":
        # Получаем текущую директорию и переходим в родительскую
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        os.chdir(parent_dir)
    else:
        # Обрабатываем пути, начинающиеся с ~/
        if path_arg.startswith("~/"):
            path_arg = os.path.expanduser(path_arg)
        
        # Проверяем существование пути
        if not os.path.exists(path_arg):
            print(f"cd: no such file or directory: {args[0]}")
            return
        
        # Проверяем, что это директория
        if not os.path.isdir(path_arg):
            print(f"cd: not a directory: {args[0]}")
            return
        
        # Меняем директорию
        try:
            os.chdir(path_arg)
        except PermissionError:
            print(f"cd: permission denied: {args[0]}")
        except Exception as e:
            print(f"cd: error: {e}")
            '''