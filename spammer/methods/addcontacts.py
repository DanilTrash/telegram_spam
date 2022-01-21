from itertools import cycle

from spammer.database import Data
from spammer.telegram import Telegram


class AddContacts:
    name = 'Add Contacts'

    def __init__(self):
        print(f'Calling {self.name}')
        self.spam_data = Data('добавление в контакты')
        self.options = Data('настройки')
        self.authorise = bool(int(self.options('authorise')[0]))
        self.targets = self.spam_data('цели').dropna().tolist()
        self.accounts = cycle(self.spam_data('аккаунты').dropna().tolist())
        self.proxy = cycle(self.spam_data('proxy').fillna('').tolist())

    def __call__(self):
        for target in self.targets:
            with Telegram(next(self.accounts), self.authorise, next(self.proxy)) as telegram:
                telegram.add_contact(str(int(target)))
        print('inviting ends')
