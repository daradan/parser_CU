import re
from typing import List

import config
from schemas import ProductSchema, PriceSchema
from models import CUPrices
import currency


def get_images(images_raw: list) -> str:
    images_list = []
    for image in images_raw:
        image: str = image.replace('250x250', '1000')
        images_list.append(f"{config.URL_I}{image}")
    return ','.join(images_list)


def get_description(description_raw: str) -> str:
    if description_raw == '<ul></ul>':
        return ''
    descriptions_list = []
    li = re.findall(r'<li>(.*?)</li>', description_raw)
    for span in li:
        if not span:
            continue
        description = re.findall(r'<span style=".*?">(.*?)</span>', span)
        descriptions_list.append(' '.join(description))
    return '\n'.join(descriptions_list)


def get_percentage(price: int, price_old: int) -> str:
    percent = round(-1 * (100 - (price * 100 / price_old)))
    if percent > 0:
        percent = f'+{percent}'
    return str(percent)


def check_lowest_price(price: float, all_prices: List[CUPrices]) -> bool:
    prices_list = []
    for data_price in all_prices:
        prices_list.append(float(data_price.price))
    price_diff = min(prices_list) - (min(prices_list) * config.PERCENTAGE / 100)
    if min(prices_list) > price > config.MIN_PRICE and price_diff > price:
        return True
    return False


def clear_all_prices(all_prices: List[CUPrices]) -> List[CUPrices]:
    if len(all_prices) <= 2:
        return all_prices
    all_prices_cleared = []
    for price in all_prices:
        if int(price.discount) == 0 or not(config.PERCENTAGE_BELOW <= int(price.discount) <= config.PERCENTAGE_ABOVE):
            all_prices_cleared.append(price)
    while len(all_prices_cleared) > config.LAST_N_PRICES:
        # all_prices_cleared.pop(-2)
        all_prices_cleared.pop()
    return all_prices_cleared


def make_image_caption(product_obj: ProductSchema, price_obj: PriceSchema, last_n_prices) -> str:
    fixed_category = fix_category(product_obj.category)
    fixed_brand = fix_category(product_obj.brand)
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"#{fixed_category} #{fixed_brand}\n\n" \
                    f"{convert_currencies(price_obj.price)}\n\n" \
                    f"{product_obj.descriptions}\n\n" \
                    f"{fix_last_n_prices(last_n_prices)}\n" \
                    f"<a href='{product_obj.url}{make_utm_tags()}'>Buy</a>\n\n" \
                    f"{config.TG_CHANNEL}"
    return image_caption


def fix_category(category: str) -> str:
    if ' / ' in category:
        return ' #'.join(category.split(' / '))

    def fix_category2(category2: str) -> str:
        need_to_replace = [' ', '-', ',']
        for change in need_to_replace:
            if change in category2:
                category2 = category2.replace(change, '_')
        return category2

    if ' & ' in category:
        temp = []
        temp_list = category.split(' & ')
        for text in temp_list:
            temp.append(fix_category2(text))
        return ' #'.join(temp)
    return fix_category2(category)


def fix_last_n_prices(last_n_prices: List[CUPrices]) -> str:
    last_n_prices_text = ''
    for data_price in last_n_prices:
        month = data_price.created.month
        day = data_price.created.day
        if data_price.discount:
            dscnt = f' ({data_price.discount}%)'
        else:
            dscnt = ''
        if month < 10:
            month = f"0{month}"
        if day < 10:
            day = f"0{day}"
        last_n_prices_text += f'{data_price.created.year}/{month}/{day} - {data_price.price} €{dscnt}\n'
    return last_n_prices_text


def make_utm_tags() -> str:
    utm_campaign = config.TG_CHANNEL[1:]
    return f"?utm_source=telegram&utm_medium=messenger&utm_campaign={utm_campaign}&utm_term={config.UTM}"


def convert_currencies(price: str) -> str:
    currencies_list = []
    converted = currency.get_or_create_currency()
    for code2, symbol in config.CURRENCIES.items():
        for code, value in converted.items():
            if code == code2:
                temp = f"~{round(float(price) * float(value), 2)}<b>{symbol}</b>"
                if code == 'EUR':
                    temp = temp.replace('~', '')
                currencies_list.append(temp)
    return ' / '.join(currencies_list)
