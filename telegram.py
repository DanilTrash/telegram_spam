import logging
from random import randint

from telethon import TelegramClient, sync
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

from database import Data


class Telegram:
    options = Data('настройки')

    def __init__(self, account, auth=True, proxy=None):
        self.account = account
        print(self.account)
        self.auth = auth
        if proxy:
            addr, port = proxy.split(':')
            proxy = ('http', addr, int(port))
        self.client = TelegramClient(
            str(self.account),
            self.options('tg_api_id')[0],
            self.options('tg_api_hash')[0],
            proxy=proxy
        )

    def __enter__(self):
        if self.auth:
            self.client.start(self.account)
        else:
            self.client.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.disconnect()

    def send_message(self, message, target):
        try:
            result = self.client.send_message(target, message)
            logging.info('message sended to %s' % target)
            return True
        except Exception as error:
            logging.error(error)
            return False

    def add_group(self, group):
        try:
            result = self.client(JoinChannelRequest(channel=group))
            logging.info('%s added' % group)
            return True
        except Exception as e:
            logging.error(e)
            return False

    def add_contact(self, target):
        try:
            contact = InputPhoneContact(client_id=randint(0, 99999), phone=target, first_name=target, last_name='')
            result = self.client(ImportContactsRequest(contacts=[contact]))
            logging.info(f'{target} added to contacts')
            return True
        except Exception as error:
            logging.error(error)
            return False

    def send_to_group(self, message, group, method):
        print(group)
        if method:
            self.add_group(group)
        try:
            self.send_message(message, group)
        except Exception as error:
            logging.error(error)

    def send_to_contact(self, message, target):
        print(target)
        self.add_contact(target)
        self.send_message(message, target)

    def invite_to_group(self, target, group):
        print(target)
        self.add_group(target)
        self.add_contact(target)
        try:
            result = self.client(InviteToChannelRequest(group, [target]))
            print(result)
        except Exception as error:
            logging.error(error)

    def sign_in_message(self):
        message = [message.text for message in self.client.iter_messages(777000)][0]
        return message

    def registration(self, code, name='Daniella'):
        self.client.sign_up(code, first_name=name)


if __name__ == '__main__':
    with Telegram('+6283838463338') as telegram:
        print(telegram.client.get_me())
