import logging
import os
import re
from random import choice
from time import sleep
from zipfile import ZipFile

import requests

from database import Data
from services import OnlineSimApi, SmsManApi
from telegram import Telegram


class Service:
    data = Data('настройки')
    account_name = data('registration_names').dropna().tolist()
    proxy = data('proxy').dropna().tolist()

    @staticmethod
    def download_telegram():
        with open(rf"telegram.zip", "wb") as f:
            ufr = requests.get(r"https://updates.tdesktop.com/tx64/tportable-x64.3.2.2.zip")
            f.write(ufr.content)
        with ZipFile(r"telegram.zip", 'r') as zip_ref:
            zip_ref.extractall()

    @staticmethod
    def get_telegram_code(telegram_message):
        message_lines = telegram_message.splitlines()
        first_line = message_lines[0].split(' ')
        code = re.sub(r'\D', '', first_line[2])
        return code


class OnlineSimService(Service, OnlineSimApi):
    name = 'OnlineSim Service'

    def __init__(self):
        OnlineSimApi.__init__(self, self.data('onlineSim_token')[0])
        self.country = self.data('onlineSim_country')[0]
        if not os.path.exists('Telegram'):
            self.download_telegram()

    def get_code(self) -> str:
        for _ in range(20):
            value = self.get_sms(self.tzid)
            print(value)
            if not value.get('msg', False):
                sleep(1)
                continue
            return value['msg'][0]['msg']
        return ''

    def __call__(self):
        self.tzid = self.get_number('telegram', self.country)
        self.number_dict = self.state(self.tzid)
        self.number = self.number_dict['number'][1:]
        try:
            with Telegram(self.number, False, choice(self.proxy)) as telegram:
                telegram.client.send_code_request(self.number, force_sms=True)
                code = self.get_code()
                if not code:
                    return False
                telegram.client.sign_up(str(code), choice(self.account_name))
                os.rename('Telegram', self.number)
                os.startfile(rf'{self.number}\telegram.exe')
                input("press enter when code sent\n")
                print(self.get_telegram_code(telegram.sign_in_message()))
                return True
        except Exception as error:
            logging.exception(error)
            return False


class SmsManService(Service, SmsManApi):
    name = 'SmsMan Service'

    def __init__(self):
        SmsManApi.__init__(self, self.data('smsMan_token')[0])
        self.country = self.data('smsMan_country')[0]
        if not os.path.exists('Telegram'):
            self.download_telegram()

    def get_code(self) -> str:
        for _ in range(20):
            value = self.get_sms(self.number['request_id'])
            print(value)
            if not value.get('sms_code', False):
                sleep(1)
                continue
            return value['sms_code']
        return ''

    def __call__(self) -> bool:
        self.number = self.get_number(self.country, 3)
        print(self.number)
        phone = self.number.get('number')
        if not phone:
            return False
        try:
            with Telegram(phone, False, choice(self.proxy)) as telegram:
                telegram.client.send_code_request(phone, force_sms=True)
                code = self.get_code()
                if not code:
                    return False
                telegram.client.sign_up(str(code), choice(self.account_name))
                os.rename('Telegram', phone)
                os.startfile(rf'{phone}\telegram.exe')
                input("press enter when code sent\n")
                print(self.get_telegram_code(telegram.sign_in_message()), '\n')
                return True
        except Exception as error:
            logging.exception(error)
            return False


class AccountRegistration:
    name = 'Account Registration'

    apis = [
        OnlineSimService(),
        SmsManService(),
    ]

    def __init__(self) -> None:
        print(f'Calling {self.name}')
        for i, api in enumerate(self.apis, 1):
            print(f'{i} -> {api.name} balance: {api.balance}')
        self.user_input = int(input('choose service: '))
        self.amount = int(input('enter amount (min - 1): '))

    def __call__(self) -> None:
        while self.amount > 0:
            try:
                service = self.apis[self.user_input - 1]
                if service():
                    self.amount -= 1
            except Exception as error:
                logging.error(error)


if __name__ == '__main__':
    acc_reg = AccountRegistration()
    acc_reg()