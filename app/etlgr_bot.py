import re
from telegram import Bot
from telegram.error import NetworkError
from time import sleep


class EtlgrBot(Bot):

    def sendMessage(self, *args, **kwargs):
        kwargs['count'] = kwargs.get('count') or 10
        try:
            return super(EtlgrBot, self).sendMessage(*args, **kwargs)

        except NetworkError as e:
            rx = re.compile('(\(\d+\))')
            kwargs['count'] -= 1

            searchRes = re.search(rx, e.message)
            currentCount = kwargs.get('count')
            if (searchRes and searchRes.group() == '(429)') and (currentCount >= 1):
                self._sleep_count(e)
                return self.sendMessage(self, *args, **kwargs)
            else:
                raise e

    def sendDocument(self, *args, **kwargs):
        kwargs['count'] = kwargs.get('count') or 10
        try:
            return super(EtlgrBot, self).sendDocument(*args, **kwargs)

        except NetworkError as e:
            rx = re.compile('(\(\d+\))')
            kwargs['count'] -= 1

            searchRes = re.search(rx, e.message)
            currentCount = kwargs.get('count')
            if (searchRes and searchRes.group() == '(429)') and (currentCount >= 1):
                self._sleep_count(e)
                return self.sendDocument(self, *args, **kwargs)
            else:
                raise e

    def sendPhoto(self, *args, **kwargs):
        kwargs['count'] = kwargs.get('count') or 10
        try:
            return super(EtlgrBot, self).sendPhoto(*args, **kwargs)

        except NetworkError as e:
            rx = re.compile('(\(\d+\))')
            kwargs['count'] -= 1

            searchRes = re.search(rx, e.message)
            currentCount = kwargs.get('count')
            if (searchRes and searchRes.group() == '(429)') and (currentCount >= 1):
                self._sleep_count(e)
                return self.sendPhoto(self, *args, **kwargs)
            else:
                raise e

    def _sleep_count(self, e):
        rmes = re.compile('( \d+)')
        strsec = re.search(rmes, e.message).group()
        seconds = int(strsec.strip())
        sleep(seconds)



