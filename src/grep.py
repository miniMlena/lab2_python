import re
from pathlib import Path
from src.errors import ShellError
from src.paths import normalize_path, find_pathes

def grep(text: str) -> None:
    """
    Поиск строк, соответствующих шаблону в файлах.
    :param text: Строка, содержащая опции, паттерн и пути
    :return: Данная функция ничего не возвращает
    """
    recursive = False
    ignore_case = False
    pattern = None
    
    if not text:
        raise ShellError("grep: missing pattern and file operand")
    
    if len(text.split()) < 2:
        raise ShellError("grep: missing operand")

    parts = text.split()
    lim = 0
    for i in range(len(parts)):
        if parts[i].startswith('-'):
            lim += 1
            if re.sub(r"[ri]+", '', parts[i]) != "-":
                raise ShellError(f"grep: invalid option -- '{parts[i]}'")
            if 'r' in parts[i]:
                recursive = True
            if 'i' in parts[i]:
                ignore_case = True
        else:
            if pattern == None:
                pattern = parts[i]
                lim += 1

    if not pattern:
        raise ShellError("grep: missing pattern")

    if lim == len(parts):
        raise ShellError("grep: missing file operand")

    # Находим пути
    paths = find_pathes(text.split(' ', lim)[lim])

    if not paths:
        raise ShellError("grep: missing file operand")
    
    # Компилируем регулярное выражение
    flags = re.IGNORECASE if ignore_case else 0
    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        raise ShellError(f"grep: invalid pattern: {e}")

    # Обрабатываем каждый путь
    for path_str in paths:
        path = normalize_path(path_str)

        grep_search(path, pattern, regex, recursive, ignore_case)

def grep_search(path: Path, pattern: str, regex: re.Pattern, recursive: bool, ignore_case: bool) -> None:
    """
    Поиск строк, соответствующих шаблону в файлах
    :param path: Путь, по которому осуществляется поиск
    :param pattern: Строка-паттерн, по которому осуществляется поиск
    :param regex: Паттерн, по которому осуществляется поиск
    :param recursive: Является ли поиск рекурсивным
    :param ignore_case: Нужно ли игнорировать регистр
    :return: Данная функция ничего не возвращает
    """
    
    if not path.exists():
        raise ShellError(f"grep: {path}: No such file or directory")

    if path.is_file():
        search_in_file(path, regex)
    
    elif path.is_dir():
        if recursive:
            for item in path.iterdir():
                if item.is_file():
                    search_in_file(item, regex)
                elif item.is_dir():
                    grep_search(item, pattern, regex, recursive, ignore_case)
        else:
            raise ShellError(f"grep: {path}: Is a directory")

def search_in_file(file_path: Path, regex: re.Pattern):
    """
    Поиск шаблона в одном файле
    :param file_path: Путь, по которому осуществляется поиск
    :param regex: Паттерн, по которому осуществляется поиск
    :return: Данная функция ничего не возвращает
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.rstrip('\n\r')  # Убираем символы новой строки
                match = regex.search(line)
                if match:
                    print(f"{file_path} : {line_num} : {line}")
    except PermissionError:
        raise ShellError(f"grep: {file_path}: Permission denied")
    except UnicodeDecodeError:
        raise ShellError(f"grep: {file_path}: Binary file")
    except Exception as e:
        raise ShellError(f"grep: {file_path}: {e}")