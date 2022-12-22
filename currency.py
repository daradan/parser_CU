import requests
from datetime import datetime, timedelta
import xmltodict
import json
from os.path import exists

import config


def get_currencies() -> dict:
    currencies = get_or_create_currency()
    return currencies


def get_or_create_currency() -> dict:
    if not exists('currency.json'):
        response = get_response()
        save_to_json(response)
    last_currencies = get_currencies_from_json()
    last_datetime: datetime = datetime.strptime(next(iter(last_currencies)), '%Y/%m/%d %H:%M:%S')
    if abs(datetime.now() - last_datetime) >= timedelta(hours=3):
        response = get_response()
        save_to_json(response)
        last_currencies = get_currencies_from_json()
    currencies = convert_currencies(last_currencies)
    return currencies


def convert_currencies(last_currencies: dict) -> dict:
    currencies = {}
    kzt = ''
    for code, value in last_currencies[next(iter(last_currencies))].items():
        if code in config.CURRENCIES:
            if code == 'EUR':
                kzt = value
                currencies['KZT'] = value
                currencies[code] = '1'
                continue
            else:
                currencies[code] = value
    for code, value in currencies.items():
        if code != 'KZT' and code != 'EUR':
            currencies[code] = str(round(float(kzt) / float(value), 2))
    return currencies


def get_currencies_from_json() -> dict:
    with open('currency.json', 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data


def get_response() -> list:
    session = requests.Session()
    today_is = datetime.today().strftime('%d.%m.%Y')
    params = {'fdate': today_is}
    response = session.get('https://nationalbank.kz/rss/get_rates.cfm', params=params)
    converted = xmltodict.parse(response.text)['rates']['item']
    return converted


def save_to_json(currencies_list: list):
    json_data = {}
    date_now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    json_data[str(date_now)] = {}
    for currency in currencies_list:
        json_data[str(date_now)].update({currency['title']: currency['description']})
    with open('currency.json', 'w', encoding='UTF-8') as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    print(get_or_create_currency())
