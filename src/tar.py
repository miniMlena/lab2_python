import tarfile
from src.errors import ShellError
from src.paths import normalize_path, find_pathes

def tar_command(text: str) -> None:
    """
    Создание TAR.GZ архива из указанного файла или директории
    :param text: Строка, содержащая путь к архивируемому файлу и к самому архиву
    :return: Данная функция ничего не возвращает
    """
    pathes = find_pathes(text)

    if len(pathes) < 2:
        raise ShellError(f"tar: missing operand")
    elif len(pathes) > 2:
        raise ShellError(f"tar: too many arguments")

    source_path = normalize_path(pathes[0])
    archive_path = normalize_path(pathes[1])
    
    if not source_path.exists():
        raise ShellError(f"tar: cannot archive '{pathes[0]}': No such file or directory")
    
    if archive_path.suffix != '.gz' and not archive_path.name.endswith('.tar.gz'):
        raise ShellError(f"tar: archive must have .tar.gz extension")
    
    try:
        with tarfile.open(archive_path, 'w:gz') as tarf:
            tarf.add(source_path, arcname=source_path.name)
        
    except Exception as e:
        if archive_path.exists():
            archive_path.unlink()
        raise ShellError(f"tar: {e}")


def untar_command(text: str) -> None:
    """
    Распаковка TAR.GZ архива в текущий каталог
    :param text: Строка, содержащая путь к распаковываемому архиву
    :return: Данная функция ничего не возвращает
    """
    pathes = find_pathes(text)

    if len(pathes) != 1:
        raise ShellError("untar: too many arguments")
    
    archive_path = normalize_path(pathes[0])
    
    if not archive_path.exists():
        raise ShellError(f"untar: cannot unpack '{pathes[0]}': No such file or directory")
    
    if archive_path.suffix != '.gz' or not archive_path.name.endswith('.tar.gz'):
        raise ShellError(f"untar: '{pathes[0]}' is not a TAR.GZ archive")
    
    try:
        with tarfile.open(archive_path, 'r:gz') as tarf:
            tarf.extractall()
        
    except Exception as e:
        raise ShellError(f"untar: {e}")