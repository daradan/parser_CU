import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MARKET = 'Computeruniverse'

LAST_N_PRICES = 15
MIN_PRICE = 50
PERCENTAGE_BELOW = -4
PERCENTAGE_ABOVE = 4
PERCENTAGE = 20
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

ALLOWED_CATEGORIES = ['AiO Liquid Cooling', 'Amplifier', 'Bean-to-Cup Coffee Machines', 'Bluetooth Sticks',
                      'Boomboxes', 'CPU Cooler & CPU Fans', 'Chargers and Power Supplies', 'Coffee Mills',
                      'Coffee Pod / Capsule Machines', 'Compact Stereos', 'Compact System Cameras',
                      'Computer Case Fans', 'Computer Cases', 'Computer Keyboard', 'Computer Mouse', 'Desktop PCs',
                      'Digital Cameras', 'Digital Sinage Monitor', 'Drawing Tablets', 'Drip Coffee Machine',
                      'Drones & RC Models', 'E-Book Readers', 'External Drive Cases', 'External Hard Drives',
                      'Fans & Cooling for cases', 'Gaming chairs', 'Headphones', 'Headsets',
                      'Headsets for Mobile / Landline Phones', 'Home Theatre Systems', 'Joysticks, Gamepads, Wheels',
                      'Keyboards', 'LED TV / LCD TV', 'Laptops / Notebooks', 'MP3 Players',
                      'Mediaplayer / Streaming Clients', 'Memory', 'Memory Card Reader ',
                      'Memory Card Readers & Adapters', 'Memory RAM', 'Mice', 'Microphones', 'Monitors',
                      'Motherboard Components', 'Motherboards', 'Mouse Pads', 'NAS -  Network Attached Storage',
                      'Nintendo Switch Accesories', 'Nintendo Switch Consoles', 'Nintendo Switch Games',
                      'Operating Systems', 'PC Barebones', 'PC Games', 'PC Lightning', 'PC Power Supply Unit',
                      'PCI Express Graphics Cards', 'Power Supplies', 'Powerbanks', 'Processors (CPUs)',
                      'Projector Screens', 'Projectors', 'Robotic Vacuum Cleaners', 'SATA Hard Drives',
                      'SD / SDHC/ SDXC Memory Cards', 'SSD Drive', 'Single Board Computer',
                      'Smartphones & Cell Phones', 'Smartwatches', 'Sony PlayStation 4 Accessorie',
                      'Sony PlayStation 4 Games', 'Sony PlayStation 5 Accessories', 'Sony PlayStation 5 Consoles',
                      'Sony PlayStation 5 Games', 'Sound Cards', 'Speakers (HiFi)', 'Tablet PCs', 'Tripods',
                      'USB Flash Drives', 'USB Hubs', 'USB-Controller', 'Water Cooling PC', 'Webcams',
                      'Weather Stations', 'WiFi Sticks / Cards', 'Wireless LAN Routers, Accesspoints',
                      'Xbox One Games', 'Xbox One accessories', 'Xbox Series X Accessories', 'Xbox Series X Consoles',
                      'Xbox Series X Games', 'eGPU Case (GPU cases)', 'espresso machine', 'network cameras',]

# STOP_CATEGORIES = ['Construction Illumination', 'Generators', 'Construction Site Radios', 'Distance Meters',
#                     'Power Tool Batteries & Chargers', 'Compressors', 'Hand Tools', 'Cordless Drills',
#                     'Milling Machines', 'Planers', 'Multi Tools', 'Table Saws', 'Angle Grinders', 'Pressure Washers',
#                     'Sweepers', 'Leaf Blowers / Leaf Vacs', 'Lawn sprinkler', 'Garden Water Pumps', 'Garden Hoses',
#                     'Garden hose management', 'Pruning Saws', 'Pruning Shears', 'Chippers / Shredders',
#                     'Electric Hedge Trimmers', 'Chainsaws', 'Cordless Electric Mower', 'Grass Trimmers',
#                     'Charcoal Grill', 'Contact Grill', 'Electric Grill', 'Gas Grill', 'Mens Grooming',
#                     'Trimmers & Clippers', 'Dental Care', 'Vacuum Cleaners', 'Kitchen Appliances',
#                     'Stand Mixers / Blenders', 'Deep Fryers', 'Hand Blenders', 'Kettles', 'Toasters',
#                     'Water Filtration', 'Juicers', 'Knife sharpeners', 'Coffee, tea and cocoa',
#                     'Wall Ovens / Built In Ovens', 'Built In Cooktops', 'Fridges / Freezers', 'Fridges',
#                     'Freestanding Dishwasher', 'Integrated Dishwashers', 'Washing Machines', 'Dryer', 'LEGO',
#                     'Playmobil', 'Carrera', 'Satellite Dishes & Accessories', 'DVB S2 Receiver', 'DVB-C Receiver',
#                     'DVB-T2 Receivers', 'HDD Recorders', 'Blu-ray / DVD Players', 'AV-Receiver', '4K Receiver',
#                     'Compact Stereos', 'Boomboxes', 'DAB Radio', 'Internet Radios', 'Amplifier', 'Turntables',
#                     'Car HiFi/Video', 'Universal Remotes', 'Hard and Soft Cases for Digital Cameras', 'Flash Units',
#                     'Gimbal', 'Battery Grips', 'Batteries for Digital Cameras',
#                     'Digital Camera Chargers & Power Supply', 'Studio Photography', 'Telephones analog cordless',
#                     'VoIP (Voice over IP)', 'Smartphone Cases / Mobile Cases', 'DVD devices', 'Blu-ray Disc Drives',
#                     'Cables & Adapters', 'HDMI Cable', 'Network Cables', 'Optic Fibre Cables',
#                     'SATA Cable / PATA-Cable', 'AVM Fritzbox WiFi Router', 'Switches',
#                     'Uninterrupted Power Supply UPS', 'APC Uninterruptible Power Supply',
#                     'Multiple Sockets & Power Cords', 'Batteries (rechargeable)', 'Shredders', 'KVM Switches',
#                     'Document Scanners / Document Servers', 'Barcode Scanner', 'Document Scanners', 'Flatbed scanner',
#                     'Handheld Wand', 'Paper Sheets', 'Ink Cartridges', 'Toners', 'Public Displays',
#                     'Monitor Accessories', 'Tablet PC Cases', 'Servers', 'Accessories Servers',
#                     'Accessories Notebooks', 'Laptop Cases', 'Mini Fridges', ]
