import re
import stat
from pathlib import Path
from datetime import datetime
from src.errors import ShellError
from src.pathes import normalize_path, find_pathes

def ls(request: str) -> None:
    """
    Реализация команды ls с поддержкой пути и опции -l
    Использование: ls [path] или ls -l [path]
    """
    # Парсинг аргументов
    '''
    path = None
    more_data = False
    
    if args:
        # Обрабатываем аргументы
        for arg in args:
            if arg.startswith('-'):
                if 'l' in arg:
                    more_data = True
            else:
                path = arg
    '''
    flag = None
    path = None
    
    if request:
        if request.startswith("-"):
            flag = request.split()[0][1::]
            request = re.sub(r"-.*", '', request, count=1)

    if request:
        pathes = find_pathes(request)
        if len(pathes) > 1:
            raise ShellError(f"ls: too many arguments")
        else: path = pathes[0]
    
    if not(flag == "l" or flag == None):
        raise ShellError(f"ls: invalid option -- '{flag.replace("l", "", 1)}'")

    # Если путь не указан, используем текущую директорию
    if path == None:
        target_path = Path.cwd()
    else:
        target_path = normalize_path(path)
    
    # Проверяем существование пути
    if not target_path.exists():
        '''
        print(f"ls: cannot access '{path}': No such file or directory")
        return   # можно через raise ShellError
        '''
        # если введёно что-то из cwd, но не указано как относительная ссылка, то мб надо обработать
        raise ShellError(f"ls: cannot access '{path}': No such file or directory")
    # Может лучше создать отдельную функцию для таких ошибок и менять ls

    if target_path.is_file():
        files = [target_path] # если путь ведёт к файлу
    else:
        files = list(target_path.iterdir())
        files.sort(key=lambda x: x.name.lower())
    
    if flag == "l":
        list_long_format(files)
    else:
        list_simple(files)

def list_simple(files):
    """Простой вывод (только имена)"""
    for file in files:
        if "'" in file.name:
            print('"' + file.name + '"')
        elif " " in file.name:
            print("'" + file.name + "'")
        else:
            print(file.name)

def list_long_format(files):
    """Подробный вывод с информацией о файлах"""
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

def get_permissions(data):
    """Преобразует числовой режим доступа в строку вида -rwxr-xr-x"""
    permissions = []
    
    # Тип файла
    if stat.S_ISDIR(data):
        permissions.append('d')
    elif stat.S_ISLNK(data):
        permissions.append('l')
    elif stat.S_ISFIFO(data):
        permissions.append('p')
    elif stat.S_ISSOCK(data):
        permissions.append('s')
    elif stat.S_ISCHR(data):
        permissions.append('c')
    elif stat.S_ISBLK(data):
        permissions.append('b')
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