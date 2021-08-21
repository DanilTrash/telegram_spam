import datetime
from configparser import ConfigParser
from time import sleep

import pandas as pd
from schedule import every, run_pending
from telethon.errors.rpcerrorlist import *
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import logging


def main():
    config = ConfigParser()
    config.read("config.ini")
    for group in pd.read_excel("Telegram.xlsx", sheet_name="группы")['группы'].dropna().tolist():
        df = pd.read_excel("Telegram.xlsx", "реклама", dtype={'text': str, 'number of account': str})[::-1]
        text = df['text'].tolist()
        numbers = df["number of account"].tolist()
        for i, number in enumerate(numbers, start=0):
            if type(number) != float:
                print('\n' + number)
                client = TelegramClient(f'+{number}', int(config["config"]["api_id"]), config["config"]["api_hash"])
                try:
                    client.start(f"+{number}")
                except Exception as e:
                    logger.warning(e, exc_info=True)
                    continue
                try:
                    with client:
                        print(group)
                        try:
                            client(JoinChannelRequest(channel=group))
                        except (FloodWaitError,
                                UsernameNotOccupiedError,
                                ChannelPrivateError,
                                ValueError) as e:
                            logger.info(e)
                            continue
                        if type(text[i]) != float:
                            try:
                                client.send_message(group, text[i])
                            except UserBannedInChannelError as e:
                                logger.info(e)
                                client.send_message('SpamBot', r'/start')
                                client.send_message('SpamBot', r'I was wrong, please release me now')
                                continue
                            except (ChatWriteForbiddenError,
                                    ChannelPrivateError,
                                    SlowModeWaitError,
                                    ChatAdminRequiredError,
                                    FloodWaitError) as e:
                                logger.info(e)
                                continue
                except (PhoneNumberBannedError,
                        UserDeactivatedBanError,
                        ConnectionError) as e:
                    print(e)
                    continue


logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

fileHandler = logging.FileHandler('log.log')
fileHandler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

try:
    if __name__ == '__main__':
        t = 80
        main()
        every(t).minutes.do(main)
        while True:
            sleep(1)
            run_pending()
except Exception as e:
    logger.critical(e, exc_info=True)
