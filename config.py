import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

MARKET = 'Computeruniverse'

LAST_N_PRICES = 10
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL = os.getenv('TG_CHANNEL')
TG_CHANNEL_ERROR = os.getenv('TG_CHANNEL_ERROR')
UTM = 'computeruniverse_deals'

URL = 'https://www.computeruniverse.net/'
URL_P = 'https://search.computeruniverse.net/search'
URL_C = 'https://webapi.computeruniverse.net/api/catalog/topmenu/'
URL_I = 'https://img.computerunivers.net'

CURRENCIES = {'EUR': '€', 'KZT': '₸', 'RUB': '₽'}

HEADERS = {
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
