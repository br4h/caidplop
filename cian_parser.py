import requests
import re
from bs4 import BeautifulSoup

# params={'deal_type': 'sale', 'engine_version': 2,
# 'object_type': 3, 'offer_type': 'suburban', 'region': 4770,
# 'with_neighbours': 0}

START_NUM = 210846981
STOP_NUM = 210847035

for i in range(START_NUM, STOP_NUM):
    response = requests.get(f'https://izhevsk.cian.ru/sale/suburban/{i}/').content
    soup = BeautifulSoup(response, features='html.parser')
    general_info = [re.sub(r'[A-z0-9<>=" \-\/\n;]', '', str(x))
                    for x in soup.find_all('li', {'data-name': 'FeatureItem'})]
    area = str(soup.find('li', {'data-name': 'AdditionalFeatureItem'})).split('<span')
    print(re.match(r'(>[А-я 0-9,.]+<)+', '>10,08 сот.<'))
    a = re.match(r'(>[А-я 0-9,.]+<)+', area[-1])
    print(a)


