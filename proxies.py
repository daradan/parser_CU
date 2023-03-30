import requests
import re
import os
import base64
import logging
import json
from time import sleep
from random import randrange
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Proxies:
    def __init__(self):
        self.session = requests.Session()
        self.count = 0

    def start(self) -> list[str]:
        logging.info('START get proxies')
        if self.if_file_older():
            free_proxy = self.from_free_proxy()
            sslproxies = self.from_sslproxies()
            proxy_list = self.from_proxy_list()
            geonode = self.from_geonode()
            spys = self.from_spys()

            merged_proxies = self.merge_proxies(
                [
                    free_proxy,
                    sslproxies,
                    proxy_list,
                    geonode,
                    spys,
                ]
            )
            # checked_proxies = self.check_proxies(merged_proxies)
            self.save_to_json(merged_proxies)
            return merged_proxies
        proxies = self.get_from_json()
        logging.info('END get proxies')
        return proxies

    def if_file_older(self) -> bool:
        if not os.path.exists('proxies.json'):
            logging.info('File not exist')
            return True
        one_hour_ago = datetime.now() - timedelta(hours=1)
        filetime = datetime.fromtimestamp(os.path.getmtime('proxies.json'))
        if filetime < one_hour_ago:
            logging.info('File is older')
            return True
        logging.info('File isn\'t older')
        return False

    def merge_proxies(self, proxies: list[list]) -> list[str]:
        merged = []
        for proxies_list in proxies:
            if not proxies_list:
                continue
            merged += proxies_list
        logging.info('Proxies merged')
        return list(set(merged))

    def save_to_json(self, merged_proxies: list[str]) -> None:
        with open('proxies.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps({'https': merged_proxies}, indent=4))
        logging.info('Proxies saved to file')

    def get_from_json(self) -> list:
        with open('proxies.json', 'r', encoding='utf-8') as f:
            proxies = json.load(f)
            logging.info('Proxies read from file')
        return proxies['https']

    def check_proxies(self, proxies: list[str]) -> list[str]:
        def send_request(proxy_for_check: str) -> bool:
            try:
                response = requests.get('https://google.kz', proxies={'https': proxy_for_check}, timeout=10)
            except:
                return False
            if response.status_code == 200:
                return True
            return False

        checked_proxies = []
        for proxy in proxies:
            if send_request(proxy):
                checked_proxies.append(proxy)
        return checked_proxies

    def from_free_proxy(self) -> list[str] | None:
        logging.info('PROXIES - start free-proxy.cz')
        url = 'http://free-proxy.cz/en/proxylist/country/all/https/ping/all'
        headers = {'Referer': 'http://free-proxy.cz/en/proxylist/category',
                   'User-Agent': os.getenv('PROXY_USER_AGENT'), }
        try:
            response = self.session.get(url, headers=headers, timeout=10)
        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"ConnectTimeout - {e}")
            if self.count < 3:
                self.count += 1
                sleep(randrange(3, 10))
                return self.from_free_proxy()
            self.count = 0
            return
        except Exception as e:
            logging.error(f"Exception - {e}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        trs = soup.find_all('tr')
        proxies = []
        for tr in trs:
            ip_encoded = tr.find_next('td', class_='left').find('script', type='text/javascript').text
            ip = base64.b64decode(re.findall(r'"(.*)"', ip_encoded)[0]).decode('utf-8')
            port = tr.find_next('span', class_='fport').text
            proxies.append(ip + ':' + port)
        return list(set(proxies))

    def from_sslproxies(self) -> list[str] | None:
        logging.info('PROXIES - start sslproxies.org')
        url = 'https://www.sslproxies.org'
        headers = {
            'authority': 'www.sslproxies.org',
            'referer': 'https://www.sslproxies.org/',
            'user-agent': os.getenv('PROXY_USER_AGENT'),
        }
        try:
            response = self.session.get(url, headers=headers)
            if response.status_code != 200:
                return
        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"ConnectTimeout - {e}")
            if self.count < 3:
                self.count += 1
                sleep(randrange(3, 10))
                return self.from_sslproxies()
            self.count = 0
            return
        except Exception as e:
            logging.error(f"Exception - {e}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_ip_list = soup.find('textarea', class_="form-control").text
        ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', raw_ip_list)
        return list(set(ips))

    def from_proxy_list(self) -> list[str] | None:
        logging.info('PROXIES - start proxy-list.download')
        url = 'https://www.proxy-list.download/api/v1/get'
        params = {'type': 'https'}
        try:
            response = self.session.get(url, params=params)
        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"ConnectTimeout - {e}")
            if self.count < 3:
                self.count += 1
                sleep(randrange(3, 10))
                return self.from_proxy_list()
            self.count = 0
            return
        except Exception as e:
            logging.error(f"Exception - {e}")
            return
        proxies = [proxy for proxy in response.text.split('\r\n') if proxy]
        return proxies

    def from_geonode(self) -> list[str] | None:
        logging.info('PROXIES - start geonode.com')
        proxies = []
        url = 'https://proxylist.geonode.com/api/proxy-list'
        params = {
            'limit': 500,
            'page': 1,
            'sort_by': 'lastChecked',
            'sort_type': 'desc',
            'protocols': 'https',
        }
        try:
            response = self.session.get(url, params=params).json()
            for proxy in response['data']:
                proxies.append(f"{proxy['ip']}:{proxy['port']}")
            return proxies
        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"ConnectTimeout - {e}")
            if self.count < 3:
                self.count += 1
                sleep(randrange(3, 10))
                return self.from_geonode()
            self.count = 0
            return
        except Exception as e:
            logging.error(f"Exception - {e}")
            return

    def from_spys(self) -> list[str] | None:
        logging.info('PROXIES - start spys.me')
        url = 'https://spys.me/proxy.txt'
        try:
            response = self.session.get(url)
            proxies = re.findall('([0-9]+(?:\.[0-9]+){3}:[0-9]+).*-S', response.text)
            return proxies
        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"ConnectTimeout - {e}")
            if self.count < 3:
                self.count += 1
                sleep(randrange(3, 10))
                return self.from_spys()
            self.count = 0
            return
        except Exception as e:
            logging.error(f"Exception - {e}")
            return


if __name__ == '__main__':
    print(Proxies().start())
