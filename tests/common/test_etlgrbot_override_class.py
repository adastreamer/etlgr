from mock import patch
from app.etlgr_bot import EtlgrBot
from telegram import Bot
from telegram.error import NetworkError

import time

BOT_TOKEN = "123:456"

CURRENT_TIME = 0


def _fakeSendMessage(obj, *args, **kwargs):
    return "I'm a fake"

def _fakeSendMessage_with500Error(obj, *args, **kwargs):
    raise NetworkError("Internal Server Error (500)")

def _fakeSendMessage_with_base_exception(obj, *args, **kwargs):
    raise BaseException("im a base exception")


def _fakeSendMessage_with429Error(obj, *args, **kwargs):
    global CURRENT_TIME
    if CURRENT_TIME < 2:
        raise NetworkError("Too Many Requests: retry after 1 (429)")
    else:
        return "SUCCESS"


def _fakeSendMessage_with429Error_deep(obj, *args, **kwargs):
    global CURRENT_TIME
    if CURRENT_TIME < 90:
        raise NetworkError("Too Many Requests: retry after 10 (429)")
    else:
        return "SUCCESS_DEEP"


def _fakeSendMessage_with429Error_deep_stack_overflow(obj, *args, **kwargs):
    global CURRENT_TIME
    if CURRENT_TIME < 1000:
        raise NetworkError("Too Many Requests: retry after 1 (429)")
    else:
        return "SUCCESS_DEEP"


def _fakeSendMessage_with429Error_unknown(obj, *args, **kwargs):
    raise NetworkError("Too Many Requests: retry after 666")

def _fakeSendMessageReturnParams(obj, *args, **kwargs):
    return args, kwargs


def fakeSleep(num):
    global CURRENT_TIME
    CURRENT_TIME += num


class TestEtlgrOverrideClass(object):

    def test_class_ordinary_behaviour(self):
        # do a basic setup
        Bot.sendMessage = _fakeSendMessage

        #
        bot = Bot(token=BOT_TOKEN)
        originalResult = bot.sendMessage(self)

        etlgrBot = EtlgrBot(token=BOT_TOKEN)
        etlgrSendResult = etlgrBot.sendMessage(self)

        assert originalResult == etlgrSendResult


    def test_class_with_base_exception_behaviour(self):
        # do a basic setup
        Bot.sendMessage = _fakeSendMessage_with_base_exception

        etlgrBot = EtlgrBot(token=BOT_TOKEN)

        try:
            etlgrBot.sendMessage(self, None, None)
        except BaseException as e:
            assert e.message == "im a base exception"

    def test_class_with_500_exception_behaviour(self):
        # do a basic setup
        Bot.sendMessage = _fakeSendMessage_with500Error

        etlgrBot = EtlgrBot(token=BOT_TOKEN)

        try:
            etlgrBot.sendMessage(self, None, None)
        except NetworkError as e:
            assert e.message == "Internal Server Error (500)"
        else:
            assert "This code should not be executed" == "exactly"

    @patch('app.etlgr_bot.sleep', fakeSleep)
    def test_class_429_behaviour(self):
        global CURRENT_TIME
        CURRENT_TIME = 0
        # do a 429 error setup
        Bot.sendMessage = _fakeSendMessage_with429Error

        etlgrBot = EtlgrBot(token=BOT_TOKEN)

        res = etlgrBot.sendMessage(self)
        assert res == "SUCCESS"

    @patch('app.etlgr_bot.sleep', fakeSleep)
    def test_class_429_deep_behaviour(self):
        global CURRENT_TIME
        CURRENT_TIME = 0
        # do a 429 error setup
        Bot.sendMessage = _fakeSendMessage_with429Error_deep
        time.sleep = fakeSleep

        etlgrBot = EtlgrBot(token=BOT_TOKEN)

        res = etlgrBot.sendMessage(self)
        assert res == "SUCCESS_DEEP"

    @patch('app.etlgr_bot.sleep', fakeSleep)
    def test_class_429_deep_stack_overflow_behaviour(self):
        global CURRENT_TIME
        CURRENT_TIME = 0
        # do a 429 error setup
        Bot.sendMessage = _fakeSendMessage_with429Error_deep_stack_overflow
        time.sleep = fakeSleep

        etlgrBot = EtlgrBot(token=BOT_TOKEN)
        try:
            etlgrBot.sendMessage(self)
        except NetworkError as e:
            assert e.message == "Too Many Requests: retry after 1 (429)"

    def test_class_params_passing_behaviour(self):
        # do a basic setup
        Bot.sendMessage = _fakeSendMessageReturnParams

        #
        bot = Bot(token=BOT_TOKEN)
        originalResult1, originalResult2 = bot.sendMessage(self, 1, 2, 3, key1='val1', key2='val2')

        etlgrBot = EtlgrBot(token=BOT_TOKEN)
        etlgrSendResult1, etlgrSendResult2 = etlgrBot.sendMessage(self, 1, 2, 3, key1='val1', key2='val2')

        assert originalResult1 == etlgrSendResult1
        assert originalResult2.get('key1') == etlgrSendResult2.get('key1')
        assert originalResult2.get('key2') == etlgrSendResult2.get('key2')

    def test_class_non_error_in_brackets_behaviour(self):
        # do a basic setup
        Bot.sendMessage = _fakeSendMessage_with429Error_unknown

        try:
            etlgrBot = EtlgrBot(token=BOT_TOKEN)
            etlgrSendResult = etlgrBot.sendMessage(self)
        except NetworkError as e:
            assert e.message == 'Too Many Requests: retry after 666'
