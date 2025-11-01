import os
from src.errors import ShellError

def history(text: str) -> None:
    """
    Вывод истории команд
    :param text: строка, содержащая количество команд
    :return: Данная функция ничего не возвращает
    """
    log_file = "shell.log"
    
    if not os.path.exists(log_file):
        raise ShellError("history: no command history found")

    n_lines = 0

    if text:
        try:
            n_lines = int(text.strip())
            if n_lines <= 0:
                raise ShellError("history: line count must be positive")
        except ValueError:
            raise ShellError("history: invalid line count")

    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Фильтруем только команды (игнорируем ошибки и другие сообщения)
        command_lines = []
        for line in lines:
            line = line.split(' ', 2)[2]
            if line and not line.startswith('ERROR:') and not line == 'command completed successfully':
                command_lines.append(line)

        if n_lines < len(command_lines):
            command_lines = command_lines[-n_lines:]
        
        if not command_lines:
            raise ShellError("history: no commands in history")
            
        start_number = max(1, len(command_lines) - n_lines + 1)
        for i, command in enumerate(command_lines, start=start_number):
            print(f"{i:4}  {command}")

    except Exception as e:
        raise ShellError(f"history: error reading history: {e}")