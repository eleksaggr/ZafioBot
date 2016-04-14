import configobj
import logging

import telepot
from telepot.delegate import per_inline_from_id, create_open

logger = logging.getLogger("ZafioBot")


def getToken():
    return configobj.ConfigObj('token.cfg')["token"]


def initLogger():
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler("bot.log")
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | [%(levelname)s] %(name)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


class InlineHandler(telepot.helper.UserHandler):

    def __init__(self, seedTuple, timeout):
        super(InlineHandler, self).__init__(seedTuple, timeout,
                                            flavors=["inline_query", "chosen_inline_result"])
        self._answerer = telepot.helper.Answerer(self.bot)

    def on_inline_query(self, message):
        logger.info("Querying...")
        id, fromId, queryString = telepot.glance(
            message, flavor="inline_query")

        if queryString == "":
            return

        def compute():
            return [{
                "type": "article",
                "id": "1",
                "title": queryString[::-1],
                "message_text": queryString[::-1]
            }]

        logger.info("Sending: {0}".format(compute()))
        self._answerer.answer(message, compute)

    def on_chosen_inline_result(self, message):
        resultId, fromId, queryString = telepot.glance(
            message, flavor="chosen_inline_result")
        logger.info("{0}: {1}".format(fromId, queryString))


def main():
    initLogger()
    logger.info("Application started...")

    bot = telepot.DelegatorBot(
        getToken(), [(per_inline_from_id(), create_open(InlineHandler, timeout=None)), ])
    logger.info("Bot registered.")

    bot.notifyOnMessage(run_forever=True)

    logger.info("Application closing.")

if __name__ == "__main__":
    main()
