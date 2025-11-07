import logging
from src.errors import ShellError
from src.constants import history_file

history_logger = logging.getLogger('history')
history_logger.setLevel(logging.INFO)
history_handler = logging.FileHandler('.history', mode='a', encoding='utf-8')
history_handler.setFormatter(logging.Formatter('%(message)s'))
history_logger.addHandler(history_handler)
history_logger.propagate = False

def log_to_history(text: str) -> None:
    history_logger.info(text)

def history(text: str) -> None:
    """
    Вывод истории команд
    :param text: строка, содержащая количество команд
    :return: Данная функция ничего не возвращает
    """
    if not history_file.exists():
        raise ShellError("history: no command history found")

    n_lines = 10 # Количество команд по умолчанию

    if text:
        try:
            n_lines = int(text)
            if n_lines <= 0:
                raise ShellError("history: line count must be positive")
        except ValueError:
            raise ShellError("history: invalid line count")

    try:
        with open(history_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        command_lines = []
        for line in lines:
            command_lines.append(line)

        # Находим с какой строки начать вывод
        start_number = max(1, len(command_lines) - n_lines + 1)

        if n_lines < len(command_lines):
            command_lines = command_lines[-n_lines:]

        for i, command in enumerate(command_lines, start=start_number):
            print(f"{i:4} {command}", end='')

    except Exception as e:
        raise ShellError(f"history: error reading history: {e}")