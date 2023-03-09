import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

MARKET = 'Computeruniverse'

LAST_N_PRICES = 15
MIN_PRICE = 50
PERCENTAGE_BELOW = -4
PERCENTAGE_ABOVE = 4
PERCENTAGE = 15
SLEEP_START = 3
SLEEP_FINISH = 20
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL = os.getenv('TG_CHANNEL')
TG_CHANNEL_ERROR = os.getenv('TG_CHANNEL_ERROR')
UTM = 'computeruniverse_deals'

URL = 'https://www.computeruniverse.net/'
URL_P = 'https://search.computeruniverse.net/search'
URL_C = 'https://webapi.computeruniverse.net/api/catalog/topmenu/'
URL_I = 'https://img.computerunivers.net'
URL_I_MISSING = 'https://raw.githubusercontent.com/daradan/img/master/icon-image-not-found-free-vector.jpg'

CURRENCIES = {'EUR': '€', 'KZT': '₸', 'RUB': '₽'}

HEADERS = {
    'origin': 'https://www.computeruniverse.net',
    'referer': 'https://www.computeruniverse.net/',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': os.getenv('USER_AGENT'),
}

filters = ' AND (parentproductid:0 OR isparenteol:true) AND (productchannel.1.published:true)'
JSON_DATA = {
    'requests': [
        {
            'indexName': 'Prod-ComputerUniverse',
            'params': {
                'clickAnalytics': True,
                'distinct': True,
                'facets': [
                    'price_ag_floored',
                    'isnew',
                    'deliverydatepreorder',
                    'deliverydatenow',
                    'hasPublicationReviews',
                    'usedproduct',
                    'manufacturer',
                ],
                'filters': f'(categoryid:38 OR categoryids:38) {filters}',
                'highlightPostTag': '</ais-highlight-0000000000>',
                'highlightPreTag': '<ais-highlight-0000000000>',
                'maxValuesPerFacet': 1000,
                'page': 0,
                'query': '',
                'ruleContexts': [
                    'facet_category_38',
                ],
                'tagFilters': '',
            },
        },
    ],
}

PARAMS = {
    'lang': '1',
    'cachecountry': 'RU',
}

CATEGORIES_FOR_NOTIFICATE = ['Laptops / Notebooks', 'Desktop PCs', 'Tablet PCs', 'Monitors', 'eGPU Case (GPU cases)',
                             'Processors (CPUs)', 'PCI Express Graphics Cards', 'Motherboards', 'Memory RAM',
                             'PC Power Supply Unit', 'SSD Drive', 'External SSD Hard Drives', 'SATA Hard Drives',
                             'Computer Cases', 'CPU Cooler & CPU Fans', 'Wireless LAN Routers, Accesspoints',
                             'Smartphones & Cell Phones', 'Action Cams', 'Smartwatches', 'Projectors',
                             'Sony PlayStation 5 Consoles', 'Nintendo Switch Consoles', 'Xbox Series X Consoles',
                             'Robotic Vacuum Cleaners', ]
