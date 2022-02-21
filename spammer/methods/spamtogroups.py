import logging
from datetime import datetime, timedelta
from time import sleep

from spammer.database import Data
from spammer.telegram import Telegram


class SpamToGroups:
    name = 'Spam To Groups'

    def __call__(self):
        while True:
            print(self.name)
            start = datetime.now()
            spam = SpamModel()
            spam()
            end = start + timedelta(seconds=spam.timer)
            print('спам начнется в {}'.format(end.strftime("%H:%M:%S")))
            sleep(spam.timer)


class SpamModel:

    def __init__(self):
        self.options = Data('настройки')
        self.authorise = bool(int(self.options('authorise')[0]))
        self.join_group = bool(int(self.options('join_group')[0]))
        self.timer_btw_acc = int(self.options('timer_btw_acc')[0])
        self.mention = bool(int(self.options('mention_group_members')[0]))
        self.timer = int(self.options('timer')[0])
        self.spam_data = Data('рассылка в группы')
        self.groups = self.spam_data('группы').dropna().tolist()
        self.accounts = self.spam_data('аккаунт').dropna().tolist()
        self.messages = self.spam_data('сообщение').fillna('').tolist()
        self.proxy = self.spam_data('proxy').fillna('').tolist()

    def __call__(self, *args, **kwargs):
        for index, account in enumerate(self.accounts):
            try:
                with Telegram(account, self.authorise, self.proxy[index]) as telegram:
                    for group in self.groups:
                        print(group)
                        if self.join_group:
                            if not telegram.add_group(group):
                                continue
                        telegram.send_message(self.messages[index], group)
            except Exception as error:
                logging.error(error)
            sleep(self.timer_btw_acc)
