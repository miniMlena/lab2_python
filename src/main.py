from pathlib import Path
from src.execute import execute
import logging

logging.basicConfig(level=logging.INFO, filename="shell.log",
                    filemode="w", format="%(asctime)s %(message)s",
                    datefmt='[%Y-%m-%d %H:%M:%S]', encoding='utf-8')

def main() -> None:
    """
    Точка входа в программу
    :return: Данная функция ничего не возвращает
    """
    print('Добро пожаловать в мини-оболочку!\nВведите --help для информации о доступных командах. ' \
    'Для выхода введите "выход" или "exit".')
    print('Welcome to mini-shell!\nType --help for information about available commands. ' \
    'To exit type "выход" or "exit".')

    while True:
        request = input(f'{Path.cwd()}$ ')

        logging.info(request)

        if request.strip().lower() in ("выход", "exit"):
            print("Exiting shell...")
            break
        
        if request.strip() == "":
            continue

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

#    py -m src.main         cd ../Documents/exps