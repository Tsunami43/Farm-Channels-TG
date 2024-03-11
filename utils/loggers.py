import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f'logs/{name}.log')

    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('\n%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

def main_logger():
    logging.basicConfig(
        level=logging.INFO,
        filename='logs/main.log',
        filemode="w",
        format="\n%(asctime)s - [%(levelname)s] -  %(name)s - " +
            "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )