import requests
import config
import os
import re
import logging

from proxies import Proxies

categories = []


def get_subcategory(category_obj):
    for subcategory in category_obj:
        if re.search('^c/', subcategory['SeName']):
            temp_dict = {
                'id': subcategory['Id'],
                'id_parent': subcategory['ParentID'],
                'name': subcategory['Name'],
                'url': subcategory['SeName']
            }
            categories.append(temp_dict)


def get_categories(session: requests.Session, proxies: list[str]) -> list[dict]:
    logging.info(f"Categories get")
    if not proxies:
        os.remove('../proxies.json')
        session.cookies.clear()
        proxies = Proxies().start()
        return get_categories(session, proxies)
    try:
        response = session.get(config.URL_C, headers=config.HEADERS, params=config.PARAMS,
                               proxies={'https': proxies[0]}, timeout=10)
        if response.status_code != 200:
            logging.info(f"Status code not 200 in proxy {proxies[0]}. Try to use next proxy")
            proxies.pop(0)
            session.cookies.clear()
            return get_categories(session, proxies)
        json_loads = response.json()
        for subcategories in json_loads:
            get_subcategory(subcategories['Categories'])
        logging.info(f"Categories get done")
        return categories
    except requests.exceptions.ConnectionError as e:
        logging.info(f"Proxy {proxies[0]} doesn't work. Try to use next proxy")
        proxies.pop(0)
        session.cookies.clear()
        return get_categories(session, proxies)


if __name__ == '__main__':
    print(get_categories(requests.Session(), Proxies().start()))

# def get_categories(session: requests.Session(), proxies: list[str]) -> list:
#     categories = [
#         {'id': 38, 'id_parent': 1745, 'name': 'Laptops / Notebooks',
#          'url': 'c/laptops-tablet-pcs-pcs/laptops-notebooks'},
#         {'id': 235, 'id_parent': 1746, 'name': 'Desktop PCs', 'url': 'c/laptops-tablet-pcs-pcs/desktop-pcs'},
#         {'id': 780, 'id_parent': 1747, 'name': 'Tablet PCs', 'url': 'c/laptops-tablet-pcs-pcs/tablet-pcs'},
#         {'id': 1001, 'id_parent': 1756, 'name': 'Monitors', 'url': 'c/computer-office/monitors-2'},
#         {'id': 1847, 'id_parent': 1715, 'name': 'eGPU Case (GPU cases)',
#          'url': 'c/hardware-components/egpu-case-gpu-cases'},
#         {'id': 66, 'id_parent': 1715, 'name': 'Processors (CPUs)', 'url': 'c/notebooks-tablets-pcs/pc-systeme'},
#         {'id': 1008, 'id_parent': 1715, 'name': 'PCI Express Graphics Cards',
#          'url': 'c/hardware-components/pci-express-graphics-cards'},
#         {'id': 73, 'id_parent': 1715, 'name': 'Motherboards', 'url': 'c/hardware-components/motherboards'},
#         {'id': 944, 'id_parent': 1715, 'name': 'Memory RAM', 'url': 'c/hardware-components/memory-2'},
#         {'id': 530, 'id_parent': 1715, 'name': 'PC Power Supply Unit', 'url': 'c/hardware-components/power-supplies'},
#         {'id': 1319, 'id_parent': 154, 'name': 'SSD Drive', 'url': 'c/hardware-components/solid-state-drives-ssd'},
#         {'id': 1024, 'id_parent': 1319, 'name': 'External SSD Hard Drives', 'url': 'c/hardware-components/external-ss'},
#         {'id': 801, 'id_parent': 154, 'name': 'SATA Hard Drives',
#          'url': 'c/hardware-components/sata-serial-ata-harddisk-drives'},
#         {'id': 225, 'id_parent': 288, 'name': 'Computer Cases', 'url': 'c/hardware-components/computer-cases-2'},
#         {'id': 535, 'id_parent': 998, 'name': 'CPU Cooler & CPU Fans',
#          'url': 'c/hardware-components/prozessor-coolers-cpu-coolers'},
#         {'id': 806, 'id_parent': 36, 'name': 'Wireless LAN Routers, Accesspoints',
#          'url': 'c/hardware-components/wireless-lan-routers-accesspoints'},
#         {'id': 766, 'id_parent': 1727, 'name': 'Smartphones & Cell Phones',
#          'url': 'c/smartphones-radio-gps/smartphones-cell-phones'},
#         {'id': 377, 'id_parent': 88, 'name': 'Action Cams', 'url': 'c/photo-video/action-camcorder'},
#         {'id': 1156, 'id_parent': 1692, 'name': 'Smartwatches', 'url': 'c/smartphones-radio-gps/smartwatches-2'},
#         {'id': 128, 'id_parent': 1777, 'name': 'Projectors', 'url': 'c/tv-hifi-video/projectors'},
#         {'id': 1870, 'id_parent': 1869, 'name': 'Sony PlayStation 5 Consoles',
#          'url': 'c/games-entertainment/sony-playstation-5-consoles'},
#         {'id': 1827, 'id_parent': 1826, 'name': 'Nintendo Switch Consoles',
#          'url': 'c/games-entertainment/nintendo-switch-consoles'},
#         {'id': 1866, 'id_parent': 1865, 'name': 'Xbox Series X Consoles',
#          'url': 'c/games-entertainment/xbox-series-x-consoles'},
#         {'id': 1476, 'id_parent': 1473, 'name': 'Robotic Vacuum Cleaners',
#          'url': 'c/home-appliance/robotic-vacuum-cleaners'},
#     ]
#     return categories

# def get_categories(session: requests.Session(), proxies: list[str]) -> list:
#     categories = [
#         # {'id': 1745, 'id_parent': 1494, 'name': 'Notebooks & Accessories', 'url': 'c/laptops-tablet-pcs-pcs/notebooks-accessories'},
#         # {'id': 1746, 'id_parent': 1494, 'name': 'Desktop PCs & Accessories', 'url': 'c/laptops-tablet-pcs-pcs/desktop-pcs-accessories'},
#         # {'id': 1749, 'id_parent': 1494, 'name': 'Servers & Accessories', 'url': 'c/laptops-tablet-pcs-pcs/servers-accessories'},
#         # {'id': 1747, 'id_parent': 1494, 'name': 'Tablet PCs & Accessories', 'url': 'c/laptops-tablet-pcs-pcs/tablet-pcs-accessories'},
#         {'id': 1756, 'id_parent': 1712, 'name': 'Monitors & Accessories', 'url': 'c/computer-office/monitors-accessories'},
#         {'id': 18, 'id_parent': 1712, 'name': 'Printers & Accessories', 'url': 'c/computer-office/printers-accessories'},
#         {'id': 85, 'id_parent': 1712, 'name': 'Printer Supplies', 'url': 'c/computer-office/printer-supplies'},
#         {'id': 932, 'id_parent': 1712, 'name': 'Scanners', 'url': 'c/computer-office/scanners'},
#         {'id': 17, 'id_parent': 1712, 'name': 'Memory', 'url': 'c/computer-office/memory'},
#         {'id': 93, 'id_parent': 1712, 'name': 'Memorycards', 'url': 'c/computer-office/memorycards'},
#         {'id': 1490, 'id_parent': 1712, 'name': 'Stationery', 'url': 'c/computer-office/stationery'},
#         {'id': 1233, 'id_parent': 1712, 'name': 'Power Supply', 'url': 'c/computer-office/power-supply'},
#         {'id': 1336, 'id_parent': 1712, 'name': 'Input Devices', 'url': 'c/computer-office/input-devices'},
#         {'id': 184, 'id_parent': 1712, 'name': 'Media (Blank Discs, Tapes, MO, etc.)', 'url': 'c/computer-office/media-blank-discs-tapes-mo-etc'},
#     ]
#     return categories
