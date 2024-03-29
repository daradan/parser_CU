import logging
from logging.handlers import RotatingFileHandler
import requests
import json
import os
from random import randrange, shuffle
from typing import List
from time import sleep

import categories
import config
import send_to_tg
import utils
from crud import CUProductsCrud, CUPricesCrud
from database import SessionLocal
from schemas import ProductSchema, PriceSchema
from models import CUProducts, CUPrices
from proxies import Proxies


class CompUnivParser:
    def __init__(self):
        self.session = requests.Session()
        self.db_session = SessionLocal()
        self.products_crud: CUProductsCrud = CUProductsCrud(session=self.db_session)
        self.prices_crud: CUPricesCrud = CUPricesCrud(session=self.db_session)
        self.proxies = Proxies().start()

    def start(self):
        logging.info(f"{config.MARKET} Parser START")
        all_categories = categories.get_categories(self.session, self.proxies)
        shuffle(all_categories)
        for category in all_categories:
            page = 0
            response = self.get_response(category, page)
            if not response:
                continue
            response = json.loads(response.text)
            products: list = response['results'][0]['hits']
            total_pages: int = response['results'][0]['nbPages']
            while page <= total_pages:
                page += 1
                sleep(randrange(config.SLEEP_START, config.SLEEP_FINISH))
                append = self.get_response(category, page)
                if not append:
                    continue
                append = json.loads(append.text)
                products.extend(append['results'][0]['hits'])
            self.parse_products(products, category['name'])
        logging.info(f"{config.MARKET} Parser END")

    def get_response(self, category: dict, page: int) -> requests.models.Response | None:
        if not self.proxies:
            os.remove('proxies.json')
            self.session.cookies.clear()
            self.proxies = Proxies().start()
            return self.get_response(category, page)
        json_data: dict = config.JSON_DATA
        json_data['requests'][0]['params']['page'] = page
        json_data['requests'][0]['params'][
            'filters'] = f"(categoryid:{category['id']} OR categoryids:{category['id']}) {config.filters}"
        json_data['requests'][0]['params']['ruleContexts'][0] = f"facet_category_{category['id']}"
        try:
            response = self.session.post(config.URL_P, headers=config.HEADERS, json=json_data,
                                         proxies={'https': self.proxies[0]}, timeout=10)
            if response.status_code != 200:
                logging.info(f"Status code not 200 in proxy {self.proxies[0]}. Try to use next proxy")
                self.proxies.pop(0)
                self.session.cookies.clear()
                return self.get_response(category, page)
        except requests.exceptions.ConnectionError as e:
            logging.info(f"Proxy {self.proxies[0]} doesn't work. Try to use next proxy")
            self.proxies.pop(0)
            self.session.cookies.clear()
            return self.get_response(category, page)
        except Exception as e:
            logging.info(f"Exception on proxy {self.proxies[0]}\n{e}")
            return None
        return response

    def parse_products(self, products: list, category: str):
        for product in products:
            # or not product.get('manufacturer', 'noname')
            if not product.get('sku') \
                    or not product.get('productid') \
                    or not product.get('name') \
                    or not product.get('url') \
                    or not product.get('bulletpoints')\
                    or not product.get('price_ag'):
                logging.info(f"{config.MARKET}, can't find some keys. {product}")
                continue
            img = product.get('image_url_set', config.URL_I_MISSING)
            if img != config.URL_I_MISSING:
                img = utils.get_images(product['image_url_set'])
            manufacturer = product.get('manufacturer')
            if not manufacturer:
                manufacturer = 'noname'
            product_obj = {
                'sku': product['sku'],
                'store_id': product['productid'],
                'name': product['name'],
                'url': f"{config.URL}{product['url']}",
                'images': img,
                'brand': manufacturer,
                'descriptions': utils.get_description(product['bulletpoints']),
                # 'category': category,
                'category': product.get('categoryname'),
            }
            product_obj = ProductSchema(**product_obj)
            price_obj = PriceSchema(price=product['price_ag'])
            self.check_data_from_db(product_obj, price_obj, category)

    def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema, category: str):
        product = self.products_crud.get_or_create(product_obj)
        price_obj.product_id = product.id
        last_price = self.prices_crud.get_last_price(product.id)
        if last_price:
            try:
                discount = utils.get_percentage(int(float(price_obj.price)), int(float(last_price.price)))
            except ZeroDivisionError as e:
                logging.error(f"division by zero")
                return
            price_obj.discount = discount
        if not last_price or price_obj.discount != '0':
            self.prices_crud.insert(price_obj)
            if not last_price:
                return
            all_prices: List[CUPrices] = self.prices_crud.get_all_prices(product.id)
            is_lowest_price = utils.check_lowest_price(float(price_obj.price), all_prices[1:])
            if is_lowest_price and utils.is_in_allowed_ctfrs(product_obj.category):
                all_prices_cleared = utils.clear_all_prices(all_prices)
                image_caption = utils.make_image_caption(product_obj, price_obj, all_prices_cleared)
                try:
                    send_tg = send_to_tg.send_as_photo(image_caption, product_obj.images.split(',')[0])
                    logging.info(f"TG status_code - {send_tg}. Product id - {product.id}")
                except:
                    return


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[
            RotatingFileHandler('CU_parser.log', mode='a+', maxBytes=10485760, backupCount=2, encoding='utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    while True:
        try:
            CompUnivParser().start()
            break
        except Exception as e:
            logging.error(e)
