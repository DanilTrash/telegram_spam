import logging

from accountregistration import AccountRegistration
from addcontacts import AddContacts
from invitetogroup import InviteToGroup
from spamtoclients import SpamToClients
from spamtogroups import SpamToGroups


class MainMenu:
    name = 'Main Menu'

    methods = [
        SpamToGroups,
        SpamToClients,
        InviteToGroup,
        AddContacts,
        AccountRegistration,
    ]

    def __init__(self):
        print(f'Calling {self.name}')
        for i, method in enumerate(self.methods, 1):
            print(f'{i} -> {method.name}')
        self.user_input = int(input('choose option: '))

    def __call__(self):
        method = self.methods[self.user_input - 1]()
        try:
            method()
        except Exception as error:
            logging.exception(error)
            return False


if __name__ == '__main__':
    while True:
        try:
            main_menu = MainMenu()
            main_menu()
        except KeyboardInterrupt as interruption:
            print(interruption)
            print('Closing job')
