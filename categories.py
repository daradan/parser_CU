### If you want scrape all categories, you need uncomment lines from 2 to 32 and comment lines from 33 to 71
# import requests
# import config
#
#
# categories = []
#
#
# def get_subcategory(category_obj):
#     for subcategory in category_obj:
#         if subcategory['Categories']:
#             get_subcategory(subcategory['Categories'])
#         else:
#             temp_dict = {
#                 'id': subcategory['Id'],
#                 'id_parent': subcategory['ParentID'],
#                 'name': subcategory['Name'],
#                 'url': subcategory['SeName']
#             }
#             categories.append(temp_dict)
#
#
# def get_categories() -> list:
#     response = requests.get(config.URL_C, headers=config.HEADERS, params=config.PARAMS)
#     json_loads = response.json()
#     for subcategories in json_loads:
#         get_subcategory(subcategories['Categories'])
#     return categories
#
#
# if __name__ == '__main__':
#     print(get_categories())
def get_categories() -> list:
    categories = [
        {'id': 38, 'id_parent': 1745, 'name': 'Laptops / Notebooks',
         'url': 'c/laptops-tablet-pcs-pcs/laptops-notebooks'},
        {'id': 235, 'id_parent': 1746, 'name': 'Desktop PCs', 'url': 'c/laptops-tablet-pcs-pcs/desktop-pcs'},
        {'id': 780, 'id_parent': 1747, 'name': 'Tablet PCs', 'url': 'c/laptops-tablet-pcs-pcs/tablet-pcs'},
        {'id': 1001, 'id_parent': 1756, 'name': 'Monitors', 'url': 'c/computer-office/monitors-2'},
        {'id': 1847, 'id_parent': 1715, 'name': 'eGPU Case (GPU cases)',
         'url': 'c/hardware-components/egpu-case-gpu-cases'},
        {'id': 66, 'id_parent': 1715, 'name': 'Processors (CPUs)', 'url': 'c/notebooks-tablets-pcs/pc-systeme'},
        {'id': 1008, 'id_parent': 1715, 'name': 'PCI Express Graphics Cards',
         'url': 'c/hardware-components/pci-express-graphics-cards'},
        {'id': 73, 'id_parent': 1715, 'name': 'Motherboards', 'url': 'c/hardware-components/motherboards'},
        {'id': 944, 'id_parent': 1715, 'name': 'Memory RAM', 'url': 'c/hardware-components/memory-2'},
        {'id': 530, 'id_parent': 1715, 'name': 'PC Power Supply Unit', 'url': 'c/hardware-components/power-supplies'},
        {'id': 1319, 'id_parent': 154, 'name': 'SSD Drive', 'url': 'c/hardware-components/solid-state-drives-ssd'},
        {'id': 1024, 'id_parent': 1319, 'name': 'External SSD Hard Drives', 'url': 'c/hardware-components/external-ss'},
        {'id': 801, 'id_parent': 154, 'name': 'SATA Hard Drives',
         'url': 'c/hardware-components/sata-serial-ata-harddisk-drives'},
        {'id': 225, 'id_parent': 288, 'name': 'Computer Cases', 'url': 'c/hardware-components/computer-cases-2'},
        {'id': 535, 'id_parent': 998, 'name': 'CPU Cooler & CPU Fans',
         'url': 'c/hardware-components/prozessor-coolers-cpu-coolers'},
        {'id': 806, 'id_parent': 36, 'name': 'Wireless LAN Routers, Accesspoints',
         'url': 'c/hardware-components/wireless-lan-routers-accesspoints'},
        {'id': 766, 'id_parent': 1727, 'name': 'Smartphones & Cell Phones',
         'url': 'c/smartphones-radio-gps/smartphones-cell-phones'},
        {'id': 377, 'id_parent': 88, 'name': 'Action Cams', 'url': 'c/photo-video/action-camcorder'},
        {'id': 1156, 'id_parent': 1692, 'name': 'Smartwatches', 'url': 'c/smartphones-radio-gps/smartwatches-2'},
        {'id': 128, 'id_parent': 1777, 'name': 'Projectors', 'url': 'c/tv-hifi-video/projectors'},
        {'id': 1870, 'id_parent': 1869, 'name': 'Sony PlayStation 5 Consoles',
         'url': 'c/games-entertainment/sony-playstation-5-consoles'},
        {'id': 1827, 'id_parent': 1826, 'name': 'Nintendo Switch Consoles',
         'url': 'c/games-entertainment/nintendo-switch-consoles'},
        {'id': 1866, 'id_parent': 1865, 'name': 'Xbox Series X Consoles',
         'url': 'c/games-entertainment/xbox-series-x-consoles'},
        {'id': 1476, 'id_parent': 1473, 'name': 'Robotic Vacuum Cleaners',
         'url': 'c/home-appliance/robotic-vacuum-cleaners'},
    ]
    return categories
