import os
import stat
import time
from pathlib import Path
from datetime import datetime

def ls(args=None):
    """
    Реализация команды ls с поддержкой пути и опции -l
    Использование: ls [path] или ls -l [path]
    """
    # Парсинг аргументов
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
    
    # Если путь не указан, используем текущую директорию
    if path is None:
        target_path = Path.cwd()
    else:
        target_path = Path(path)
        # Если указан относительный путь, делаем его абсолютным относительно текущей директории
        if not target_path.is_absolute():
            target_path = Path.cwd() / target_path
    
    # Проверяем существование пути
    if not target_path.exists():
        print(f"ls: cannot access '{path}': No such file or directory")
        return
    
    # Если путь - файл, показываем только его
    if target_path.is_file():
        files = [target_path]
    else:
        # Получаем список файлов и директорий
        files = list(target_path.iterdir())
        files.sort(key=lambda x: x.name.lower())  # Сортируем по имени
    
    # Выводим результат
    if more_data:
        _print_long_format(files)
    else:
        _print_simple(files)

def _print_simple(files):
    """Простой вывод (только имена)"""
    for file in files:
        print(file.name)

def _print_long_format(files):
    """Подробный вывод с информацией о файлах"""
    total_blocks = 0
    file_stats = []
    
    # Собираем статистику для всех файлов
    for file in files:
        try:
            stat_info = file.stat()
            total_blocks += stat_info.st_blocks
            file_stats.append((file, stat_info))
        except OSError as e:
            print(f"Error accessing {file}: {e}")
            continue
    
    # Выводим общий размер блоками (как в ls -l)
    print(f"total {total_blocks}")
    
    # Выводим информацию о каждом файле
    for file, stat_info in file_stats:
        # Права доступа
        permissions = _get_permissions(stat_info.st_mode)
        
        # Количество жестких ссылок
        nlinks = stat_info.st_nlink
        
        # Размер файла
        size = stat_info.st_size
        
        # Время модификации
        mtime = datetime.fromtimestamp(stat_info.st_mtime)
        mtime_str = mtime.strftime('%b %d %H:%M')
        
        # Имя файла
        name = file.name
        
        # Если это символическая ссылка, показываем куда она ведет
        if file.is_symlink():
            try:
                target = os.readlink(file)
                name = f"{name} -> {target}"
            except OSError:
                name = f"{name} -> [broken link]"
        
        print(f"{permissions} {nlinks:>2} {size:>8} {mtime_str} {name}")

def _get_permissions(mode):
    """Преобразует числовой режим доступа в строку вида -rwxr-xr-x"""
    permissions = []
    
    # Тип файла
    if stat.S_ISDIR(mode):
        permissions.append('d')
    elif stat.S_ISLNK(mode):
        permissions.append('l')
    elif stat.S_ISFIFO(mode):
        permissions.append('p')
    elif stat.S_ISSOCK(mode):
        permissions.append('s')
    elif stat.S_ISCHR(mode):
        permissions.append('c')
    elif stat.S_ISBLK(mode):
        permissions.append('b')
    else:
        permissions.append('-')
    
    # Права для владельца
    permissions.append('r' if mode & stat.S_IRUSR else '-')
    permissions.append('w' if mode & stat.S_IWUSR else '-')
    permissions.append('x' if mode & stat.S_IXUSR else '-')
    
    # Права для группы
    permissions.append('r' if mode & stat.S_IRGRP else '-')
    permissions.append('w' if mode & stat.S_IWGRP else '-')
    permissions.append('x' if mode & stat.S_IXGRP else '-')
    
    # Права для остальных
    permissions.append('r' if mode & stat.S_IROTH else '-')
    permissions.append('w' if mode & stat.S_IWOTH else '-')
    permissions.append('x' if mode & stat.S_IXOTH else '-')
    
    return ''.join(permissions)

# Пример использования в мини-оболочке:
if __name__ == "__main__":
    # Тестирование
    print("Simple ls:")
    ls()
    
    print("\nDetailed ls:")
    ls(["-l"])
    
    print("\nLs with path:")
    ls([".."])
    
    print("\nDetailed ls with path:")
    ls(["-l", ".."])