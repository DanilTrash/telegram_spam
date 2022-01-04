import argparse
import logging
import sys
from configparser import ConfigParser
from time import sleep

from onlinesimru import GetUser, GetNumbers


class OnlineSimApi:

    @property
    def name(self):
        return 'OnlineSimApi'

    def __init__(self, api_key):
        self.sim = GetNumbers(api_key)
        self.user = GetUser(api_key)

    @property
    def balance(self) -> str:
        try:
            value = self.user.balance()["balance"]
            return value
        except Exception as error:
            logging.error(error)
            return 'Cant get balance'

    def get_number(self, service, country) -> str:
        tzid = self.sim.get(service, country=country)
        return tzid

    def numbers(self):
        return self.sim.state()

    def get_sms(self, tzid) -> dict:
        code = self.sim.stateOne(tzid, 1)
        return code

    def state(self, tzid):
        if not tzid:
            return {}
        return self.sim.stateOne(tzid)


class Client:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("settings.ini")
        self.api_key = self.config['OnlineSim']['api_key']
        if len(sys.argv) == 1:
            sys.argv = [__file__, '92', 'telegram']
        parser = argparse.ArgumentParser()
        parser.add_argument('country')
        parser.add_argument('service')
        self.args = parser.parse_args()
        self.service = OnlineSimApi(self.api_key)

    def __call__(self, *args, **kwargs):
        number = self.service.get_number(self.args.service, self.args.country)
        print(number)
        while True:
            sms = self.service.get_sms(number)
            print(sms)
            sleep(1)


if __name__ == '__main__':
    client = Client()
    client()
