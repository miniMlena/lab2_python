import logging
from pathlib import Path

undo_logger = logging.getLogger('undo')
undo_logger.setLevel(logging.INFO)
undo_handler = logging.FileHandler('.trash', mode='w', encoding='utf-8')
undo_handler.setFormatter(logging.Formatter('%(message)s'))
undo_logger.addHandler(undo_handler)
undo_logger.propagate = False

def log_remove(file_path: Path) -> None:
    """
    Логироавание операции удаления
    :param file_path: Путь до удалённого файла
    :return: Данная функция ничего не возвращает
    """
    try:
        if file_path.is_file():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('\n', '\\n').replace('\r', '\\r')
            undo_logger.info(f"rm_file path:{file_path} content:{content}")
            
        elif file_path.is_dir():
            undo_logger.info(f"rm_dir path:{file_path}")
            
            for item in file_path.rglob('*'):
                if item.is_file():
                    try:
                        with open(item, 'r', encoding='utf-8') as f:
                            content = f.read()
                        content = content.replace('\n', '\\n').replace('\r', '\\r')
                        relative_path = str(item.relative_to(file_path))
                        undo_logger.info(f"file:{relative_path} content:{content}")
                    except Exception as e:
                        print(f"Warning: could not read file {item}: {e}")
                        relative_path = str(item.relative_to(file_path))
                        undo_logger.info(f"file:{relative_path} content:[ERROR]")
                
                elif item.is_dir():
                    relative_path = str(item.relative_to(file_path))
                    undo_logger.info(f"dir:{relative_path}")
            
            undo_logger.info("---END_DIR---")
            
    except Exception as e:
        print(f"Warning: could not log remove operation: {e}")

def log_copy(dest_path: Path) -> None:
    """
    Логирование операции копирования
    :param dest_path: Путь до копии файла
    :return: Данная функция ничего не возвращает
    """
    try:
        if dest_path.is_file():
            undo_logger.info(f"cp_file dest:{dest_path}")
        elif dest_path.is_dir():
            undo_logger.info(f"cp_dir dest:{dest_path}")
    except Exception as e:
        print(f"Warning: could not log copy operation: {e}")

def log_move(source_path: Path, dest_path: Path) -> None:
    """
    Логирование операции перемещения
    :paran source_path: Путь, по которому файл находился раньше
    :param dest_path: Новый путь до файла
    :return: Данная функция ничего не возвращает
    """
    try:
        if source_path.is_file():
            undo_logger.info(f"mv_file source:{source_path} dest:{dest_path}")
        elif source_path.is_dir():
            undo_logger.info(f"mv_dir source:{source_path} dest:{dest_path}")
    except Exception as e:
        print(f"Warning: could not log move operation: {e}")

def remove_error_from_trash() -> None:
    '''
    Удаления лога об операции, на случай если при исполнении возникнет ошибка
    (в случае с rm и mv логирование происходит до исполнения,
    так как иначе нужная для лога информация уже будет стёрта)
    :param: Данная функция ничего не принимает
    :return: Данная функция ничего не возвращает
    '''
    from src.constants import trash_file
    with open(trash_file, "r", encoding="utf-8") as f:
        lines = [line.replace('\0', '') for line in f.readlines()]

    op_start = -1
    for i in range(len(lines)-1, -1, -1):
        if lines[i].startswith(('rm_', 'cp_', 'mv_')):
            op_start = i
            break
        
    new_lines = lines[:op_start]

    with open(trash_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)