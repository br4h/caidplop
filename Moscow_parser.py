import requests
from bs4 import BeautifulSoup as bs

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}


def domofond_parser(start_page, end_page, page_counter=True):
    pages = []
    for i in range(start_page, end_page + 1):
        pages.append(
            requests.get(f'https://www.domofond.ru/prodazha-uchastkizemli-izhevsk-c2017?Page={i}', headers=HEADERS)
        )
        if page_counter:
            print(i)

    counter = 1
    for page in pages:
        soup = bs(page.content, 'html.parser')
        items = soup.findAll('a', class_='long-item-card__item___ubItG search-results__itemCardNotFirst___3fei6')[1:]
        for el in items:
            try:
                response_nested = requests.get(f'https://www.domofond.ru{el["href"]}', headers=HEADERS)
            except requests.exceptions.ConnectionError:
                continue
            soup_nested = bs(response_nested.content, 'html.parser')
            items_nested = soup_nested.findAll('div', class_='detail-information__row___29Fu6')

            # ОЦЕНКА РАЙОНА
            ratings = {}
            try:
                for rating in soup_nested.findAll('div', 'area-rating__row___3y4HH'):
                    ratings[rating.find('div', 'area-rating__label___2Y1bh').get_text(strip=True)] \
                        = rating.find('div', 'area-rating__score___3ERQc').get_text(strip=True)
            except AttributeError:
                # Если
                print('Фигня')
                continue

            try:
                proximity, area, price = [str(items_nested[x]).split('<span>')[-1] for x in range(1, 4)]
                area = str(area).replace('соток', 'сот')
                price = price[:price.find("₽") - 1].replace(' ', '')
            except IndexError:
                # Если цена в объявлении договорная
                print('Фигня 2')
                continue
            with open('../result/domofond_result_new.txt', 'a') as f:
                f.write(
                    f'Площадь: {area[:area.find("<")]};Расстояниедогорода: {proximity[:proximity.find("<")]};Цена: {price};{";".join([f"{x}: {y}" for x, y in ratings.items()])}\n'
                )
                print(f'записан номер {counter}')
            counter += 1


domofond_parser(1, 10)
