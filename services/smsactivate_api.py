import argparse
import sys
from time import sleep

import requests
from configparser import ConfigParser


class SmsActivateApi:
    api_url = 'https://api.sms-activate.org/stubs/handler_api.php?'

    @property
    def name(self) -> str:
        return 'SmsActivateApi'

    def __init__(self, api_key) -> None:
        self.__api_key = api_key

    @property
    def balance(self) -> str:
        params = {
            'action': 'getBalance',
            'api_key': self.__api_key,
        }
        value = requests.get(f'{self.api_url}', params=params).text
        return value

    def get_number(self, country_id: str, application_id: str) -> str:
        params = {
            'action': 'getNumber',
            'api_key': self.__api_key,
            'service': application_id,
            'country': country_id
        }
        value = requests.get(f'{self.api_url}', params=params).text
        return value

    def get_status(self, request_id: str) -> str:
        params = {
            'action': 'getStatus',
            'api_key': self.__api_key,
            'id': request_id
        }
        value = requests.get(f'{self.api_url}', params=params).text
        return value

    def get_countries(self) -> dict:
        params = {
            'api_key': self.__api_key,
            'action': 'getCountries'
        }
        value = requests.get(f'{self.api_url}', params=params).json()
        return value


class Client:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("settings.ini")
        self.api_key = self.config['SmsActivate']['api_key']
        if len(sys.argv) == 1:
            sys.argv = [__file__, '0', 'ig']
        parser = argparse.ArgumentParser()
        parser.add_argument('country')
        parser.add_argument('service')
        self.args = parser.parse_args()
        self.service = SmsActivateApi(self.api_key)

    def __call__(self, *args, **kwargs):
        c = 0
        while True:
            c += 1
            print(c)
            number = self.service.get_number(self.args.country, self.args.service)
            if number != 'NO_NUMBERS':
                print(number)
                break


if __name__ == '__main__':
    client = Client()
    print(client.service.balance)
    client()
