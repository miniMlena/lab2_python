import os
from src.errors import ShellError
from src.pathes import normalize_path, find_pathes

def cat(text: str) -> None:
    ''''''
    if not text:
        raise ShellError("cat: no arguments")
    else:
        pathes = find_pathes(text)
        if len(pathes) > 1:
            raise ShellError(f"cat: too many arguments")
        target_file = normalize_path(pathes[0])
    
    if not target_file.exists():
        raise ShellError(f"cat: {target_file}: No such file or directory")
    
    if target_file.is_dir():
        raise ShellError(f"cat: {target_file}: Is a directory")
    
    if not os.access(target_file, os.R_OK):
        print(f"cat: {target_file}: Permission denied")    # Проверка прав доступа
        
    try:
        with open(target_file, 'r', encoding='utf-8') as file:
            print(file.read(), end='')

    except Exception as e:
        raise ShellError(f"cat: {target_file}: Error reading file: {e}")