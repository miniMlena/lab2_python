import re
import stat
from pathlib import Path
from datetime import datetime
from src.errors import ShellError
from src.paths import normalize_path, find_pathes

def ls(text: str) -> None:
    """
    Вывод списка файлов и каталогов, находящихся в указанной директории.
    С опцией -l также выводятся права доступа, размер и время изменения файлов
    :param text: Строка с опциями и путём к файлу или директории (возможно пустая)
    :return: Данная функция ничего не возвращает
    """
    flag = None
    path = None

    # Находим опции
    if text:
        if text.startswith("-"):
            flag = text.split()[0][1::]
            text = re.sub(r"-[^\s]*", '', text, count=1)

    if not(flag == "l" or flag == None):
        raise ShellError(f"ls: invalid option -- '{flag.replace("l", "", 1)}'")
    
    # Находим пути
    if text:
        pathes = find_pathes(text)
        if len(pathes) > 1:
            raise ShellError(f"ls: too many arguments")
        else: path = pathes[0]

    if path == None:
        target_path = Path.cwd()
    else:
        target_path = normalize_path(path)
    
    if not target_path.exists():
        raise ShellError(f"ls: cannot access '{path}': No such file or directory")

    if target_path.is_file():
        files = [target_path] # если путь ведёт к файлу
    else:
        files = list(target_path.iterdir())
        files.sort(key=lambda x: x.name.lower())
    
    if flag == "l":
        list_long_format(files)
    else:
        for file in files:
            if "'" in file.name:
                print('"' + file.name + '"')
            elif " " in file.name:
                print("'" + file.name + "'")
            else:
                print(file.name)

def list_long_format(files: list) -> None:
    """
    Вспомогательная функция для вывода подробной информации о файлах
    :param files: Список путей к файлам
    :return: Данная функция ничего не возвращает
    """
    file_stats = []
    
    for file in files:
        try:
            stat_info = file.stat()
            file_stats.append((file, stat_info))
        except OSError as e:
            print(f"ls: cannot access {file}: {e}")
            continue
    
    for file, stat_info in file_stats:
        permissions = get_permissions(stat_info.st_mode)    # права доступа
        
        size = stat_info.st_size    # размер
        
        mtime = datetime.fromtimestamp(stat_info.st_mtime)    # время изменения
        mtime_str = mtime.strftime('%b %d %H:%M')
        
        if "'" in file.name or " " in file.name:    # имя
            name = '"' + file.name + '"'
        else:
            name = file.name
        
        print(f"{permissions} {size:>6} {mtime_str} {name}")

def get_permissions(data: int) -> str:
    """
    Вспомогательная функция для преобразования информации
    о режиме доступа к файлу в формат, принятый в linux
    :param data: Число, содержащее информацию о типе файла и правах доступа
    :return: Строка вида -rwxr-xr-x
    """
    permissions = []
    
    if stat.S_ISDIR(data):
        permissions.append('d')
    else:
        permissions.append('-')
    
    # Права владельца
    permissions.append('r' if data & stat.S_IRUSR else '-')
    permissions.append('w' if data & stat.S_IWUSR else '-')
    permissions.append('x' if data & stat.S_IXUSR else '-')
    
    # Права группы
    permissions.append('r' if data & stat.S_IRGRP else '-')
    permissions.append('w' if data & stat.S_IWGRP else '-')
    permissions.append('x' if data & stat.S_IXGRP else '-')
    
    # Права остальных
    permissions.append('r' if data & stat.S_IROTH else '-')
    permissions.append('w' if data & stat.S_IWOTH else '-')
    permissions.append('x' if data & stat.S_IXOTH else '-')
    
    return ''.join(permissions)