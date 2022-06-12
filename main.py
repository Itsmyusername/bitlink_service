import os
import requests
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    parametrs = {
        'long_url': f'{url}',
        'title': f'short_link_{url}',
    }
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=parametrs)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, url):
    local_url = urlparse(url)
    headers = {
        'Authorization': f'Bearer {token}',
    }

    params = {
        'unit': 'day',
        'units': '-1',
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{local_url.netloc+local_url.path}/clicks/summary',
        headers=headers,
        params=params)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, url):
    local_url = urlparse(url)
    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{local_url.netloc+local_url.path}',
        headers=headers
    )
    return response.ok

if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='Описание что делает программа')
    parser.add_argument('url', help='Ссылка на сайт')
    args = parser.parse_args()
    url = args.url
    bitly_api_token = os.getenv('BITLY_API_TOKEN')
    #url = input('Введите сайт для создания короткой ссылки: ')

    if is_bitlink(bitly_api_token, url):
        bit_count_click = count_clicks(bitly_api_token, url)
        print('Сумма кликов:', bit_count_click)
    else:
        bitlink = shorten_link(bitly_api_token, url)
        print('Битлинк', bitlink)
