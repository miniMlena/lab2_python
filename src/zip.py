import zipfile
from src.errors import ShellError
from src.paths import normalize_path, find_pathes

def zip_command(text: str) -> None:
    """
    Создание ZIP архива из указанного файла или директории
    :param text: Строка, содержащая путь к архивируемому файлу и к самому архиву
    :return: Данная функция ничего не возвращает
    """
    pathes = find_pathes(text)

    if len(pathes) < 2:
        raise ShellError(f"zip: missing operand")
    elif len(pathes) > 2:
        raise ShellError(f"zip: too many arguments")

    zipping_path = normalize_path(pathes[0])
    archive_path = normalize_path(pathes[1])
    
    if not zipping_path.exists():
        raise ShellError(f"zip: cannot zip '{pathes[0]}': No such file or directory")
    
    if archive_path.suffix != '.zip':
        raise ShellError(f"zip: archive must have .zip extension")
    
    try:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if zipping_path.is_file(): # Для возможности архивировать отдельные файлы
                zipf.write(zipping_path, zipping_path.name)
            elif zipping_path.is_dir():
                for item_path in zipping_path.rglob('*'):
                    arcname = item_path.relative_to(zipping_path)
                    if item_path.is_file():
                        zipf.write(item_path, arcname)
                    elif item_path.is_dir():
                        # Позволяет добавлять пустые каталоги в архив (по умолчанию zipfile их не добавляет)
                        zipf.writestr(str(arcname) + '/', '')
        
    except Exception as e:
        if archive_path.exists():
            archive_path.unlink()
        raise ShellError(f"zip: {e}")

def unzip_command(text: str) -> None:
    """
    Распаковка ZIP архива в текущий каталог
    :param text: Строка, содержащая путь к распаковываемому архиву
    :return: Данная функция ничего не возвращает
    """
    pathes = find_pathes(text)

    if len(pathes) != 1:
        raise ShellError("unzip: too many arguments")
    
    archive_path = normalize_path(pathes[0])
    
    if not archive_path.exists():
        raise ShellError(f"unzip: cannot unpack '{pathes[0]}': No such file or directory")
    
    if archive_path.suffix.lower() != '.zip':
        raise ShellError(f"unzip: '{pathes[0]}' is not a ZIP archive")
    
    try:
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            zipf.extractall()
        
    except Exception as e:
        raise ShellError(f"unzip: {e}")