import requests
import re
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

response = requests.get('https://www.avito.ru/rossiya/zemelnye_uchastki', headers=HEADERS).content
soup = BeautifulSoup(response, features='html.parser')
i = 1
for link in soup.find_all('a', 'snippet-link'):
    elem = str(link).split('" ')[1]
    print(elem)
    try:
        response = requests.get('https://www.avito.ru/' + elem[elem.find('"') + 1:]).content
    except requests.exceptions.TooManyRedirects:
        pass
    soup = BeautifulSoup(response, features='html.parser')
    params = re.sub(r'[a-z<>=" \-\/\n;]', '', str(soup.find('div', 'item-params')))
    price = re.search(r'\d+', str(soup.find('span', 'js-item-price'))).group(0)
    with open('newnew_result.txt', 'a') as f:
        f.write(f'{params},')
        f.write(f'{price};\n')
        print(f'записан номер {i}')
    i += 1
