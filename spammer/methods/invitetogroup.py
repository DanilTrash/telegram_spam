from itertools import cycle

from spammer.database import Data
from spammer.telegram import Telegram


class InviteToGroup:
    name = 'Invite To Group'

    def __init__(self):
        print(f'Calling {self.name}')
        self.options = Data('настройки')
        self.authorise = bool(int(self.options('authorise')[0]))
        self.timer_btw_acc = int(self.options('timer_btw_acc')[0])
        self.spam_data = Data('раскрутка')
        self.target_group = cycle(self.spam_data('группа'))
        self.targets = self.spam_data('участники для приглашения').tolist()
        self.accounts = cycle(self.spam_data('аккаунты').dropna().tolist())
        self.proxy = cycle(self.spam_data('proxy').fillna('').tolist())

    def __call__(self, *args, **kwargs):
        for target in self.targets:
            with Telegram(next(self.accounts), self.authorise, next(self.proxy)) as telegram:
                telegram.invite_to_group(str(int(target)), next(self.target_group))
        print('inviting ends')
