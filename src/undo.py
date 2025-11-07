from pathlib import Path
from src.errors import ShellError
from src.constants import trash_file

def undo() -> None:
    """
    Отменяет последнюю операцию
    :param: Данная функция ничего не принимает
    :return: Данная функция ничего не возвращает
    """
    try:
        if not trash_file.exists():
            raise ShellError(f'Missing {trash_file} file')

        with open(trash_file, "r", encoding="utf-8") as f:
            lines = [line.replace('\0', '') for line in f.readlines()]
        if not lines:
            raise ShellError("Nothing to undo")
            
        # Находим начало последней операции (ищем c конца)
        op_start = -1
        for i in range(len(lines)-1, -1, -1):
            if lines[i].startswith(('rm_', 'cp_', 'mv_')):
                op_start = i
                break

        op_lines = lines[op_start:]
        op_type = op_lines[0].split(' ', 1)[0]
# Удаление
        if op_type == "rm_file":
            parts = op_lines[0].split(' ', 1) # Отделяем название операции от пути
            rest_parts = parts[1].split(' content:', 1)
            file_path = Path(rest_parts[0].replace('path:', ''))
            content = rest_parts[1] if len(rest_parts) == 2 else ''

            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True)
            content = content.replace('\\n', '\n').replace('\\r', '\r')[:-1] #Возвращаем символы переноса и убираем \n в конце
            print(content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                    
            remove_operation_from_trash(op_start)
        
        elif op_type == "rm_dir":
            # Формат: remove_dir path:/path/to/dir
            parts = op_lines[0].split(' ', 1)
            dir_path = Path(parts[1].replace('path:', '')[:-1]) # Убираем \n в конце строки
            dir_path.mkdir()
            
            i = 1 # отслеживает количество обработанных строк
            while i < len(op_lines) and op_lines[i] != "---END_DIR---":
                if op_lines[i].startswith("file:"):
                    # Формат: file:relative/path content:content
                    file_line = op_lines[i]
                    # Разделяем на 2 части: file:путь и содержимое
                    file_parts = file_line.split(' content:', 1)
                    
                    if len(file_parts) == 2:
                        file_part = file_parts[0].replace("file:", "")
                        content = file_parts[1]
                    else:
                        file_part = file_line.replace("file:", "")
                        content = ""
                    
                    file_path = dir_path / file_part
                    if not file_path.parent.exists():
                        file_path.parent.mkdir(parents=True, exist_ok=True)

                    if content == "[ERROR]":
                        file_path.touch() # Для файлов с ошибками создаем пустой файл
                    else:
                        #Возвращаем символы переноса и убираем \n в конце:
                        content = content.replace('\\n', '\n').replace('\\r', '\r')[:-1]
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)

                elif op_lines[i].startswith("dir:"):
                    # Формат: dir:relative/path
                    dir_line = op_lines[i].replace("dir:", "")[:-1]
                    dir_i_path = dir_path / dir_line
                    if not dir_i_path.exists():
                        dir_i_path.mkdir(parents=True, exist_ok=True)

                i += 1
            
            remove_operation_from_trash(op_start) #Удаляем запись о действии из .trash

#Копирование            
        elif op_type == "cp_file":
            # Формат: cp_file dest:/path/dest.txt
            parts = op_lines[0].split(" ", 1)
            dest_path = Path(parts[1].replace("dest:", "")[:-1])
            dest_path.unlink()

            remove_operation_from_trash()
                
        elif op_type == "cp_dir":
            parts = op_lines[0].split(" ", 1)
            dest_path = Path(parts[1].replace("dest:", "")[:-1])

            import shutil
            shutil.rmtree(dest_path)

            remove_operation_from_trash()
                
#Перемещение 
        elif op_type == "mv_file":
            # Формат: mv_file source:/old/path dest:/new/path
            parts = op_lines[0].split(" ")
            source_path = Path(parts[1].replace("source:", ""))
            dest_path = Path(parts[2].replace("dest:", "")[:-1])

            import shutil
            shutil.move(dest_path, source_path)

            remove_operation_from_trash()

        elif op_type == "mv_dir":
            # Формат: mv_dir source:/old/path dest:/new/path
            parts = op_lines[0].split(" ")
            source_path = Path(parts[1].replace("source:", ""))
            dest_path = Path(parts[2].replace("dest:", "")[:-1])

            import shutil
            shutil.move(dest_path, source_path)

            remove_operation_from_trash()

    except Exception as e:
        raise ShellError(f"undo: {e}")
        
    
def remove_operation_from_trash(op_start: int = -1) -> None:
    """
    Удаляет отменённую операцию из файла .trash
    :param op_start: Номер строки, с которой нужно начать удаление, по умолчанию -1
    :return: Данная функция ничего не возвращает
    """
    with open(trash_file, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
        
    new_lines = all_lines[:op_start]

    with open(trash_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)