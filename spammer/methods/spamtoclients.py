from itertools import cycle
from time import sleep

from spammer.database import Data
from spammer.telegram import Telegram


class SpamToClients:
    name = 'Spam To Clients'

    def __init__(self):
        print(f'Calling {self.name}')
        self.options = Data('настройки')
        self.authorise = bool(int(self.options('authorise')[0]))
        self.join_group = bool(int(self.options('join_group')[0]))
        self.timer_btw_acc = int(self.options('timer_btw_acc')[0])
        self.spam_data = Data('рассылка клиентам')
        self.targets = self.spam_data('цели').dropna().tolist()
        self.accounts = cycle(self.spam_data('аккаунты').dropna().tolist())
        self.messages = cycle(self.spam_data('сообщение').fillna('').tolist())
        self.proxy = cycle(self.spam_data('proxy').fillna('').tolist())

    def __call__(self, *args, **kwargs):
        for target in self.targets:
            with Telegram(next(self.accounts), self.authorise, next(self.proxy)) as telegram:
                telegram.send_to_contact(next(self.messages), str(int(target)))
            sleep(self.timer_btw_acc)
        print('spamming to clients ends')


if __name__ == '__main__':
    spam = SpamToClients()
    spam()
