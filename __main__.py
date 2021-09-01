import datetime
from configparser import ConfigParser
from time import sleep

import pandas as pd
from telethon.errors.rpcerrorlist import *
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from logger import logger

LOGGER = logger('main')


def main():
    for group in pd.read_excel("Telegram.xlsx", sheet_name="группы")['группы'].dropna().tolist():
        df = pd.read_excel("Telegram.xlsx", "реклама", dtype={'text': str, 'number of account': str})[::-1]
        text = df['text'].tolist()
        numbers = df["number of account"].tolist()
        for i, number in enumerate(numbers):
            if type(number) == float:
                continue
            print(f'\n+{number}')
            print(group)
            client = TelegramClient(f'+{number}',
                                    int(config["telegram"]["tg_api_id"]),
                                    config["telegram"]["tg_api_hash"],
                                    )
            try:
                if config['telegram']['skip_unauthorized'] == '1':
                    client.start(f'+{number}', code_callback=lambda d: False)
                else:
                    client.start(f'+{number}')
            except TypeError:
                LOGGER.warning(f'telegram +{number} unauthorized')
                continue
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
            if type(text[i]) == float:
                client.disconnect()
                continue
            try:
                client.send_message(group, text[i])
                client.disconnect()
            except UserBannedInChannelError as e:
                LOGGER.info(e)
                client.send_message('SpamBot', r'/start')
                client.send_message('SpamBot', r'I was wrong, please release me now')
                client.disconnect()
                continue
            except Exception as e:
                LOGGER.info(e)
                client.disconnect()
                continue


if __name__ == '__main__':
    while True:
        config = ConfigParser()
        config.read("config.ini")
        timer = int(config['telegram']['timer'])
        try:
            main()
        except Exception as error:
            LOGGER.exception(error)
        time = datetime.datetime.now() + datetime.timedelta(minutes=timer)
        LOGGER.info(f'Спам запустится в {time.strftime("%H:%M")}')
        sleep(timer * 60)
