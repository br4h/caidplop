import requests
import re
from bs4 import BeautifulSoup

response = requests.get('https://www.avito.ru/rossiya/zemelnye_uchastki').content
soup = BeautifulSoup(response, features='html.parser')
i = 1
for link in soup.find_all('a', 'snippet-link'):
    elem = str(link).split('" ')[1]
    response = requests.get('https://www.avito.ru/' + elem[elem.find('"') + 1:]).content
    soup = BeautifulSoup(response, features='html.parser')
    params = re.sub(r'[a-z<>=" \-\/\n;]', '', str(soup.find('div', 'item-params')))
    price = re.search(r'\d+', str(soup.find('span', 'js-item-price'))).group(0)
    with open('result.txt', 'a') as f:
        f.write(f'{params},')
        f.write(f'{price};\n')
        print(f'записан номер {i}')
    i += 1
