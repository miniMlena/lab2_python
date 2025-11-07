from pathlib import Path
import logging
from src.execute import execute
from src.history import log_to_history

# Настраиваем логирование в shell.log
logging.basicConfig(
level=logging.INFO,
filename="shell.log",
filemode="w",
format="%(asctime)s %(message)s",
datefmt='[%Y-%m-%d %H:%M:%S]',
encoding='utf-8')

def main() -> None:
    """
    Точка входа в программу
    :return: Данная функция ничего не возвращает
    """
    print('Добро пожаловать в мини-оболочку!\nВведите --help для информации о доступных командах. ' \
    'Для выхода введите "выход" или "exit".\n')
    print('Welcome to mini-shell!\nType --help for information about available commands. ' \
    'To exit type "выход" or "exit".')

    while True:
        request = input(f'{Path.cwd()}$ ')

        if request.strip() == "":
            continue

        logging.info(request)
        log_to_history(request)

        if request.strip().lower() in ("выход", "exit"):
            print("Exiting shell...")
            break

        try:
            execute(request)
            logging.info("command completed successfully")
        except KeyboardInterrupt:
            print("Exiting shell...")
            break
        except Exception as e:
            print(e)
            logging.error(f"ERROR: {e}")

if __name__ == "__main__":
    main()