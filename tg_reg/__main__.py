import logging
from configparser import ConfigParser
from os import rename, startfile, getcwd
from random import choice
from zipfile import ZipFile
from requests import get
from telethon.errors.rpcerrorlist import *
from telethon.sync import TelegramClient
from time import sleep
from onlinesim_api import OnlineSim
import sms_man_api

config = ConfigParser()
config.read("config.ini")
API_ID = int(config["config"]["api_id"])
API_HASH = config["config"]["api_hash"]

name = str(choice(open('names').read().splitlines()))
logger = logging.getLogger('main')
consolehandler = logging.StreamHandler()
fileHandler = logging.FileHandler('log.log')
logger.addHandler(fileHandler)
logger.addHandler(consolehandler)
formatter = logging.Formatter('%(asctime)s ~ %(name)s ~ %(levelname)s: %(message)s')
fileHandler.setFormatter(formatter)
logger.setLevel(logging.INFO)
consolehandler.setLevel(logging.INFO)
fileHandler.setLevel(logging.INFO)


def desktop_login(number):
    print('downloading telegram')
    f = open(rf"телеграммы\telegram.zip", "wb")
    ufr = get(r"https://updates.tdesktop.com/tx64/tportable-x64.2.8.1.zip")
    f.write(ufr.content)
    f.close()
    with ZipFile(r"телеграммы\telegram.zip", 'r') as zip_ref:
        zip_ref.extractall(rf"телеграммы")
    rename(rf"телеграммы\Telegram",
           rf"телеграммы\{number}")
    print('login to desktop')
    startfile(rf"телеграммы\{number}\telegram.exe")
    input("press enter when code sent\n")
    code(number)


def code(number):
    client = TelegramClient(number, API_ID, API_HASH)
    try:
        client.connect()
        print([message.text for message in client.iter_messages(777000)][0])
        client.disconnect()
    except PhoneNumberBannedError as e:
        print(e)
    except UserDeactivatedBanError as e:
        print(e)


def auto(country):
    sim = OnlineSim()
    tzid = sim.get_number('telegram', country)
    number = sim.state(tzid)['number']
    print(number)
    client = TelegramClient(number, API_ID, API_HASH)
    try:
        client.connect()
        client.send_code_request(number, force_sms=True)
        client.sign_up(sim.code(tzid), first_name=name)
        client.disconnect()
        desktop_login(number)
    except PhoneNumberBannedError as e:
        logging.exception(e)
    except SessionPasswordNeededError as e:
        logging.exception(e)
    except FloodWaitError as e:
        logging.exception(e)
    except PhoneNumberInvalidError as e:
        logging.exception(e)


def manual():
    number = input('Enter the phone: ')
    print(number)
    client = TelegramClient(number, API_ID, API_HASH)
    try:
        client.connect()
        client.send_code_request(number, force_sms=True)
        code_input = input('Enter the code: ')
        client.sign_up(code_input, first_name=name)
        client.disconnect()
        desktop_login(number)
    except PhoneNumberBannedError as e:
        logging.exception(e)
    except SessionPasswordNeededError as e:
        logging.exception(e)
    except FloodWaitError as e:
        logging.exception(e)
    except PhoneNumberInvalidError as e:
        logging.exception(e)


def get_code(request_id):
    for i in range(6):
        req = sms_man_api.get_sms(request_id)
        try:
            return req['sms_code']
        except KeyError:
            if i == 0:
                print(req['error_code'])
            if i == 1:
                print(req['error_msg'])
            sleep(7)
    return False


def sms_man(country):
    get_number_json = sms_man_api.get_number(country, 3)
    try:
        print(get_number_json['get_number_json'])
        return False
    except KeyError:
        pass
    try:
        request_id = get_number_json['request_id']
    except KeyError as error:
        logger.warning(error)
        return False
    number = '+' + get_number_json['number']
    print(number)
    client = TelegramClient(number, API_ID, API_HASH)
    try:
        client.connect()
        client.send_code_request(number, force_sms=True)
        if not get_code(request_id):
            return False
        client.sign_up(get_code(request_id), first_name=name)
        client.disconnect()
        desktop_login(number)
    except PhoneNumberBannedError as e:
        logger.info(e, exc_info=True)
    except SessionPasswordNeededError as e:
        logger.info(e, exc_info=True)
    except FloodWaitError as e:
        logger.info(e, exc_info=True)
    except PhoneNumberInvalidError as e:
        logger.info(e, exc_info=True)


if __name__ == '__main__':
    user_input = input('Choice service\nSmsMan - 1\nOnlineSim - 2\n=>')
    # elif user_input == '2':
    #     manual()
    if user_input == '1':
        while True:
            sms_man(config['sms_man']['sms_man_country'])
    elif user_input == '2':
        while True:
            auto(config['online_sim']['country'])
    else:
        print('Wrong!')
        sleep(5)

    # code('+62083803612232')
