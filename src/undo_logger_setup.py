import logging

def setup_undo_logger():
    '''
    Функция для настройки файла .trash
    :return: Данная функция ничего не возвращает
    '''
    logger = logging.getLogger('undo_logger')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        undo_handler = logging.FileHandler('.trash')
        undo_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(message)s')
        undo_handler.setFormatter(formatter)

        logger.addHandler(undo_handler)
    
    return logger

undo_logger = setup_undo_logger()