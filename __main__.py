import logging

# from spammer.methods.accountregistration import AccountRegistration
# from spammer.methods.addcontacts import AddContacts
# from spammer.methods.invitetogroup import InviteToGroup
# from spammer.methods.spamtoclients import SpamToClients
from spammer.methods.spamtogroups import SpamToGroups


class MainMenu:
    name = 'Main Menu'

    methods = [
        SpamToGroups,
        # SpamToClients,
        # InviteToGroup,
        # AddContacts,
        # AccountRegistration,
    ]

    def __init__(self):
        print(f'Calling {self.name}')
        for i, method in enumerate(self.methods, 1):
            print(f'{i} -> {method.name}')
        self.user_input = int(input('choose option: '))

    def __call__(self):
        try:
            method = self.methods[self.user_input - 1]()
            method()
        except Exception as error:
            logging.exception(error)
            return False


if __name__ == '__main__':
    __version__ = '1.0.2'
    print('version: %s' % __version__)
    while True:
        try:
            main_menu = MainMenu()
            main_menu()
        except Exception as error:
            logging.error(error)
