import datetime
from configparser import ConfigParser
from time import sleep

import pandas as pd
from telethon.errors.rpcerrorlist import *
from telethon import TelegramClient, sync
from telethon.tl.functions.channels import JoinChannelRequest

from logger import logger

LOGGER = logger('main')


def dataframe():
    return pd.read_excel("Telegram.xlsx", "реклама", dtype={'text': str, 'number of account': str})[::-1]


def main():
    numbers = dataframe()["number of account"].tolist()
    for i, number in enumerate(numbers):
        for group in pd.read_excel("Telegram.xlsx", sheet_name="группы")['группы'].dropna().tolist():
            if type(number) == float:
                continue
            print(f'+{number}')
            print(group)
            client = TelegramClient(f'+{number}', int(config["telegram"]["tg_api_id"]),
                                    config["telegram"]["tg_api_hash"])
            if config['telegram']['skip_unauthorized'] == '0':
                try:
                    client.start(f'+{number}')
                except Exception as error:
                    LOGGER.error(error)
                    continue
            client.connect()
            if config['telegram']['join_group'] == '1':
                try:
                    client(JoinChannelRequest(channel=group))
                except Exception as e:
                    LOGGER.error(e)
                    client.disconnect()
                    continue
            text = dataframe()['text'].tolist()
            if type(text[i]) == float:
                client.disconnect()
                continue
            try:
                client.send_message(group, text[i])
                timer_btw_tg = int(config['telegram']['timer_btw_tg'])
                sleep(timer_btw_tg)
                client.disconnect()
            except Exception as e:
                LOGGER.error(e)
                client.disconnect()
                continue


if __name__ == '__main__':
    while True:
        config = ConfigParser()
        config.read("config.ini")
        try:
            main()
        except Exception as error:
            LOGGER.exception(error)
        timer = int(config['telegram']['timer'])
        time = datetime.datetime.now() + datetime.timedelta(minutes=timer)
        LOGGER.info(f'Спам запустится в {time.strftime("%H:%M")}')
        sleep(timer * 60)
