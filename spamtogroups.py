import logging
from time import sleep

from database import Data
from telegram import Telegram


class SpamToGroups:
    name = 'Spam To Groups'

    def __call__(self):
        while True:
            spam = SpamModel()
            spam()
            print(f'sleeping for {spam.timer} seconds')
            sleep(spam.timer)


class SpamModel(SpamToGroups):

    def __init__(self):
        print(self.name)
        self.options = Data('настройки')
        self.authorise = bool(int(self.options('authorise')[0]))
        self.join_group = bool(int(self.options('join_group')[0]))
        self.timer_btw_acc = int(self.options('timer_btw_acc')[0])
        self.timer = int(self.options('timer')[0])
        self.spam_data = Data('рассылка в группы')
        self.groups = self.spam_data('группы').dropna().tolist()
        self.accounts = self.spam_data('аккаунт').dropna().tolist()
        self.messages = self.spam_data('сообщение').fillna('').tolist()
        self.proxy = self.spam_data('proxy').fillna('').tolist()

    def __call__(self, *args, **kwargs):
        print('spamming')
        for index, account in enumerate(self.accounts):
            try:
                with Telegram(account, self.authorise, self.proxy[index]) as telegram:
                    for group in self.groups:
                        telegram.send_to_group(self.messages[index], group, self.join_group)
            except Exception as error:
                logging.exception(error)
            sleep(self.timer_btw_acc)
        print('spam to groups ends')


if __name__ == '__main__':
    spam = SpamToGroups()
    spam()
