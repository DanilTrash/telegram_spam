import logging
from configparser import ConfigParser

from onlinesimru import GetUser, GetNumbers
from logger import logger

config = ConfigParser()
config.read("config.ini")
onlineSim_token = config['online_sim']['onlineSim_token']  # todo
LOGGER = logger('tg_reg', file='tg_reg.log')


class OnlineSim:
    def __init__(self):
        self.sim = GetNumbers(onlineSim_token)
        self.user = GetUser(onlineSim_token)

    def balance(self):
        return self.user.balance()["balance"]

    def numbers(self):
        return self.sim.state()

    def get_number(self, service, country):
        return self.sim.get(service, country=country)

    def code(self, tzid):
        while True:
            print("Ждем код с OnlineSim")
            try:
                return self.sim.wait_code(tzid, 1)
            except Exception as error:
                LOGGER.error(error)
                continue

    def state(self, tzid):
        return self.sim.stateOne(tzid)

    def tariffs1(self, ):
        return self.sim.tariffs()


if __name__ == '__main__':
    service = input("сервис: ")
    country = input("country: ")
    sim = OnlineSim()
    tzid = sim.get_number(service, country)
    print(sim.state(tzid)['number'])
    while True:
        try:
            print(sim.state(tzid)['msg'][0]['msg'])
            break
        except KeyError as error:
            pass
        except Exception as error:
            logging.exception(error)
            break
