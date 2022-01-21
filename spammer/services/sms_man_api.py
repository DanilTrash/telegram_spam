import argparse
import sys
from time import sleep

import requests
from configparser import ConfigParser


class SmsManApi:
    api_url_v1 = 'http://api.sms-man.ru/stubs/handler_api.php'
    api_url_v2 = 'http://api.sms-man.ru/control'

    @property
    def name(self):
        return 'SmsMan'

    def __init__(self, api_key):
        self.__api_key = api_key

    @property
    def balance(self) -> dict:
        params = {
            'token': self.__api_key
        }
        value = requests.get(f'{self.api_url_v2}/get-balance', params=params).json()
        return value

    def get_number(self, country_id, application_id):
        params = {
            # 'action': 'getNumber',
            'token': self.__api_key,
            'application_id': application_id,
            'country_id': country_id
        }
        value = requests.get(f'{self.api_url_v2}/get-number', params=params).json()
        return value

    def get_sms(self, request_id):
        params = {
            'token': self.__api_key,
            'request_id': request_id
        }
        value = requests.get(f'{self.api_url_v2}/get-sms', params=params).json()
        return value

    def get_limits(self, country_id=None, application_id=None):
        params = {
            'token': self.__api_key,
            'country_id': country_id,
            'application_id': application_id
        }
        value = requests.get(f'{self.api_url_v2}/limits', params=params).content
        return value

    def get_prices(self, country=None):
        params = {
            'token': self.__api_key,
            'country': country
        }
        value = requests.get(f'{self.api_url_v2}/get-prices', params=params).json()
        return value

    def get_countries_apiv2(self):
        params = {
            'token': self.__api_key
        }
        value = requests.get(f'{self.api_url_v2}/countries', params=params).json()
        return value

    def get_countries_apiv1(self):
        params = {
            'api_key': self.__api_key,
            'action': 'getCountries'
        }
        value = requests.get(f'{self.api_url_v1}', params=params).json()
        return value

    def get_applications(self):
        params = {
            'token': self.__api_key
        }
        value = requests.get(f'{self.api_url_v2}/applications', params=params).json()
        return value


class Client:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("settings.ini")
        self.api_key = self.config['SmsMan']['api_key']
        if len(sys.argv) == 1:
            sys.argv = [__file__, '15', '3']
        parser = argparse.ArgumentParser()
        parser.add_argument('country')
        parser.add_argument('service')
        self.args = parser.parse_args()
        self.service = SmsManApi(self.api_key)

    def __call__(self, *args, **kwargs):
        number = self.service.get_number(self.args.country, self.args.service)
        print(number)
        while True:
            print(self.service.get_sms(number['request_id']))
            sleep(1)


if __name__ == '__main__':
    client = Client()
    client()
