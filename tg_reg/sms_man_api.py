from time import sleep

import requests

TOKEN = '7jum0G6_tqXLCIZoAbMo8luIh6HW2IgQ'
URL = 'http://api.sms-man.ru/control'


def balance():
    return requests.get(f'{URL}/get-balance?token={TOKEN}').json()


def limits(country_id, application_id):
    return requests.get(f'{URL}/limits?token={TOKEN}&country_id=${country_id}&application_id=${application_id}')


def get_number(country_id, application_id):
    return requests.get(f'{URL}/get-number?token={TOKEN}&country_id={country_id}&application_id={application_id}').json()


def get_sms(request_id):
    return requests.get(f'{URL}/get-sms?token={TOKEN}&request_id={request_id}').json()


def set_status(request_id, status):
    return requests.get(f'{URL}/set-status?token={TOKEN}&request_id={request_id}&status={status}').json()


def countries():
    return requests.get(f'{URL}/countries?token={TOKEN}').json()


def applications():
    return requests.get(f'{URL}/applications?token={TOKEN}').json()


if __name__ == '__main__':
    for i in countries():
        print(i)