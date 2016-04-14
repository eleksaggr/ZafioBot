import configobj
import logging


def getToken():
    return configobj.ConfigObj('token.cfg')["token"]


def initLogger():
    logger = logging.getLogger("ZafioBot")
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler("bot.log")
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | [%(levelname)s] %(name)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def main():
    logger = initLogger()
    logger.info("Application started...")

    logger.info("Application closing.")

if __name__ == "__main__":
    main()
