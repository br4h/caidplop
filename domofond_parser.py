from bs4 import BeautifulSoup as bs
import requests

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 YaBrowser/20.7.0.894 Yowser/2.5 Safari/537.36"
}

START_PAGE, MAX_PAGE = 1, 77
pages = []
for i in range(START_PAGE, MAX_PAGE + 1):
    pages.append(
        requests.get(f'https://www.domofond.ru/prodazha-uchastkizemli-izhevsk-c2017?Page={i}', headers=HEADERS)
    )
    print(i)
data = {}  # словарь входных данных
counter = 1

for response in pages:
    soup = bs(response.content, 'html.parser')
    items = soup.findAll('a', 'long-item-card__item___ubItG search-results__itemCardNotFirst___3fei6')[1:]
    for el in items:
        response_nested = requests.get(f'https://www.domofond.ru{el["href"]}',
                                       headers=HEADERS)
        soup_nested = bs(response_nested.content, 'html.parser')
        items_nested = soup_nested.findAll('div', 'detail-information__row___29Fu6')

        # ОЦЕНКА РАЙОНА
        ratings = {}
        try:
            for rating in soup_nested.findAll('div', 'area-rating__row___3y4HH'):
                ratings[rating.find('div', 'area-rating__label___2Y1bh').get_text(strip=True)] \
                    = rating.find('div', 'area-rating__score___3ERQc').get_text(strip=True)
        except AttributeError:
            print('Stuff')
            continue

        for el_nested in items_nested:
            params = el_nested.get_text(strip=True).split(':')
            if params[0] == 'Цена' or params[0] == 'Расстояние от центра' or params[0] == 'Площадь':
                data[params[0]] = params[1]

        try:
            price = data['Цена'].replace('₽', '').replace(' ', '')
            area = data['Площадь'].replace('соток', 'сот').replace('сотки', 'сот')
            distance = data['Расстояние от центра']

            with open('domofond_parser.txt', 'a', encoding='utf-8') as f:
                f.write(
                    f'Площадь:{area};Расстояниедогорода:{distance};Цена:{price};{";".join([f"{x}: {y}" for x, y in ratings.items()])}\n'
                )
                print(f'записан номер {counter}')
                counter += 1
                data.clear()
                ratings.clear()
        except Exception:
            data.clear()
            ratings.clear()
            print('*')
