import logging
import requests
from random import randrange, shuffle
from time import sleep

import categories
import config
import send_to_tg
import utils
from crud import CUProductsCrud, CUPricesCrud
from database import SessionLocal
from schemas import ProductSchema, PriceSchema


class CompUnivParser:
    def __init__(self):
        self.session = requests.Session()
        self.db_session = SessionLocal()
        self.products_crud: CUProductsCrud = CUProductsCrud(session=self.db_session)
        self.prices_crud: CUPricesCrud = CUPricesCrud(session=self.db_session)

    def start(self):
        logging.info(f"{config.MARKET} Parser Start")
        all_categories = categories.get_categories()
        shuffle(all_categories)
        for category in all_categories:
            page = 0
            response = self.get_response(category, page)
            if not response:
                continue
            products: list = response['results'][0]['hits']
            total_pages: int = response['results'][0]['nbPages']
            while page <= total_pages:
                page += 1
                sleep(randrange(3, 20))
                append = self.get_response(category, page)
                if not append:
                    continue
                products.extend(append['results'][0]['hits'])
            self.parse_products(products, category['name'])

    def get_response(self, category: dict, page: int) -> dict | None:
        json_data: dict = config.JSON_DATA
        json_data['requests'][0]['params']['page'] = page
        json_data['requests'][0]['params']['filters'] = f"(categoryid:{category['id']} OR categoryids:{category['id']}) {config.filters}"
        json_data['requests'][0]['params']['ruleContexts'][0] = f"facet_category_{category['id']}"
        products = self.session.post(config.URL_P, headers=config.HEADERS, json=json_data)
        if products.status_code != 200:
            logging.exception(f"{config.MARKET}, {category}, ERROR: {products}")
            return None
        return products.json()

    def parse_products(self, products: list, category: str):
        for product in products:
            if not product.get('sku') \
                    or not product.get('productid') \
                    or not product.get('name') \
                    or not product.get('url') \
                    or not product.get('image_url_set') \
                    or not product.get('manufacturer')\
                    or not product.get('bulletpoints'):
                continue
            product_obj = {
                'sku': product['sku'],
                'store_id': product['productid'],
                'name': product['name'],
                'url': f"{config.URL}{product['url']}",
                'images': utils.get_images(product['image_url_set']),
                'brand': product['manufacturer'],
                'descriptions': utils.get_description(product['bulletpoints']),
                'category': category,
            }
            product_obj = ProductSchema(**product_obj)
            price_obj = PriceSchema(price=product['price_ag'])
            self.check_data_from_db(product_obj, price_obj)

    def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema):
        product = self.products_crud.get_or_create(product_obj)
        price_obj.product_id = product.id
        last_price = self.prices_crud.get_last_price(product.id)
        if last_price:
            discount = utils.get_percentage(int(float(price_obj.price)), int(float(last_price.price)))
            price_obj.discount = discount
        if not last_price or price_obj.discount != '0':
            self.prices_crud.insert(price_obj)
            if int(price_obj.discount) <= -15:
                last_n_prices = self.prices_crud.get_last_n_prices(product.id)
                image_caption = utils.make_image_caption(product_obj, price_obj, last_n_prices)
                if len(product_obj.images.split(',')) > 1:
                    send_tg = send_to_tg.send_as_media_group(image_caption, product_obj)
                else:
                    send_tg = send_to_tg.send_as_photo(image_caption, product_obj.images)
                if send_tg != 200:
                    return


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[logging.FileHandler('../CU_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    CompUnivParser().start()
