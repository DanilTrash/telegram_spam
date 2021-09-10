import os
from configparser import ConfigParser
from os import rename, startfile
from random import choice
from zipfile import ZipFile
from requests import get
from telethon.errors.rpcerrorlist import *
from telethon.sync import TelegramClient
from time import sleep
from onlinesim_api import OnlineSim
import sms_man_api
from logger import logger

LOGGER = logger('tg_reg', file='tg_reg.log')


def desktop_login(number):
    print('downloading telegram')
    f = open(rf"telegrams\telegram.zip", "wb")
    ufr = get(r"https://updates.tdesktop.com/tx64/tportable-x64.2.8.1.zip")
    f.write(ufr.content)
    f.close()
    with ZipFile(r"telegrams\telegram.zip", 'r') as zip_ref:
        zip_ref.extractall(rf"telegrams")
    rename(rf"telegrams\Telegram",
           rf"telegrams\{number}")
    print('login to desktop')
    startfile(rf"telegrams\{number}\telegram.exe")
    input("press enter when code sent\n")
    code(number)


def code(number):
    client = TelegramClient(number, API_ID, API_HASH)
    try:
        client.connect()
        LOGGER.info([message.text for message in client.iter_messages(777000)][0])
        client.disconnect()
    except (PhoneNumberBannedError, UserDeactivatedBanError) as e:
        LOGGER.error(e)


def auto(country, service='telegram'):
    while True:
        sim = OnlineSim()
        try:
            tzid = sim.get_number(service, country)
            number = sim.state(tzid)['number']
            LOGGER.info(number)
            client = TelegramClient(number, API_ID, API_HASH)
            client.connect()
            client.send_code_request(number, force_sms=True)
            name = str(choice(open('names.txt').read().splitlines()))
            client.sign_up(sim.code(tzid), first_name=name)
            client.disconnect()
            desktop_login(number)
        except Exception as e:
            LOGGER.error(e)
        finally:
            sleep(3)


def manual():
    number = input('Enter the phone: ')
    LOGGER.info(number)
    client = TelegramClient(number, API_ID, API_HASH)
    try:
        client.connect()
        client.send_code_request(number, force_sms=True)
        code_input = input('Enter the code: ')
        name = str(choice(open('names.txt').read().splitlines()))
        client.sign_up(code_input, first_name=name)
        client.disconnect()
        desktop_login(number)
    except Exception as e:
        LOGGER.error(e)


def get_code(request_id):
    for i in range(12):
        req = sms_man_api.get_sms(request_id)
        try:
            return req['sms_code']
        except KeyError:
            if i == 0:
                LOGGER.info(req['error_code'])
            else:
                LOGGER.info(req['error_msg'])
            sleep(6)
    return False


def sms_man(country, service='tg'):
    LOGGER.info(sms_man_api.countries()[int(country)].get('name'), sms_man_api.limits(country).get(service))
    while True:
        get_number_list = sms_man_api.get_number(country, service)
        if get_number_list[0] == 'NO_NUMBERS':
            LOGGER.info(get_number_list[0])
            continue
        if get_number_list[0] == 'NO_BALANCE':
            LOGGER.info(get_number_list[0])
            return False
        if get_number_list[0] == 'BAD_KEY':
            LOGGER.info('НЕВЕРНЫЙ КЛЮЧ АПИ')
            return False
        try:
            request_id = get_number_list[1]
        except KeyError:
            LOGGER.info('Нет доступных номеров')
            return False
        number = '+' + get_number_list[2]
        LOGGER.info(number)
        client = TelegramClient(number, API_ID, API_HASH)
        try:
            client.connect()
            client.send_code_request(number, force_sms=True)
            if not get_code(request_id):
                continue
            name = str(choice(open('names.txt').read().splitlines()))
            client.sign_up(get_code(request_id), first_name=name)
            client.disconnect()
            desktop_login(number)
        except Exception as e:
            LOGGER.error(e)


def main():
    user_input = input('Choose service\n1 - SmsMan\n2 - OnlineSim\n3 - Manual\n>>> ')
    if user_input == '1':
        sms_man(config['sms_man']['country'])
    elif user_input == '2':
        auto(config['online_sim']['country'])
    elif user_input == '3':
        manual()
    else:
        LOGGER.info('Wrong!')


if __name__ == '__main__':
    try:
        config = ConfigParser()
        config.read(f"config.ini")
        API_ID = int(config["telegram"]["tg_api_id"])
        API_HASH = config["telegram"]["tg_api_hash"]
        if not os.path.exists('telegrams'):
            os.mkdir('telegrams')
        while True:
            main()
    except Exception as error:
        LOGGER.exception(error)
