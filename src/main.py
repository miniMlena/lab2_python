from pathlib import Path
from src.execute import execute
import logging

logging.basicConfig(level=logging.INFO, filename="shell.log",
                    filemode="w", format="%(asctime)s %(message)s",
                    datefmt='[%Y-%m-%d %H:%M:%S]', encoding='utf-8')

def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    #print('Добро пожаловать в мини-оболочку! Доступные команды для выполнения: .' \
    #'Для выхода введите "выход" или "exit".')
    #print('Welcome to mini-shell! Available commands: . To exit type "выход" or "exit".')

    while True:
        request = input(f'{Path.cwd()}$ ')

        logging.info(request)

        if request.strip().lower() in ("выход", "exit"):
            print("Exiting programm...")
            break

        try:
            execute(request)
            logging.info("command completed successfully")
        except Exception as e:
            print(e)
            logging.error(f"ERROR: {e}")

if __name__ == "__main__":
    main()

#    py -m src.main         cd ../Documents/exps