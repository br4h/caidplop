import requests
import re
from bs4 import BeautifulSoup

# params={'deal_type': 'sale', 'engine_version': 2,
# 'object_type': 3, 'offer_type': 'suburban', 'region': 4770,
# 'with_neighbours': 0}

START_NUM = 210846981
STOP_NUM = 210847035
REGEX = r'(>[А-я 0-9,.]+<)+'
counter = 1

for i in range(START_NUM, STOP_NUM):
    response = requests.get(f'https://izhevsk.cian.ru/sale/suburban/{i}/').content
    soup = BeautifulSoup(response, features='html.parser')
    general_info = [re.sub(r'[A-z0-9<>=" \-\/\n;]', '', str(x))
                    for x in soup.find_all('li', {'data-name': 'FeatureItem'})]
    raw_area = str(soup.find('div', {'data-name': 'Description'})).split('<div')[5]
    area = re.sub(r'^[A-z А-я</> ]', '', str(raw_area[raw_area.find('>'):])).split()[0]
    raw_price = str(soup.find('span', {'itemprop': 'price'}))
    price = raw_price.split('"')[1].replace(' ', '')[:-1]
    with open('cian_result.txt', 'a') as f:
        try:
            f.write(f'Площадь:{area} сот.Расстояниедогорода:НЕТ,{price},Инфраструктура:{" ".join(general_info)};\n')
        except UnicodeEncodeError:
            print(area, price, general_info)
        print(f'Номер {counter} записан')
    counter += 1
