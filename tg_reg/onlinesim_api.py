import logging

from onlinesimru import GetUser, GetNumbers
from onlinesimru.Extentions import RequestException


class OnlineSim:
    def __init__(self):
        self.token = "76d8377e27690ecbe2153174c22104eb"
        self.sim = GetNumbers(self.token)
        self.user = GetUser(self.token)

    def balance(self):
        while True:
            try:
                return self.user.balance()["balance"]
            except Exception as e:
                logging.exception(e)

    def numbers(self):
        while True:
            try:
                return self.sim.state()
            except Exception as e:
                logging.exception(e)

    def get_number(self, service, country):
        while True:
            try:
                return self.sim.get(service, country=country)
            except Exception as e:
                logging.exception(e)

    def code(self, tzid):
        while True:
            print("Ждем код с OnlineSim")
            try:
                return self.sim.wait_code(tzid, 1)
            except Exception as e:
                logging.exception(e)

    def state(self, tzid):
        while True:
            try:
                return self.sim.stateOne(tzid)
            except Exception as e:
                logging.exception(e)

    def tariffs1(self, ):
        while True:
            try:
                return self.sim.tariffs()
            except Exception as e:
                logging.exception(e)


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
