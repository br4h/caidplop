from bs4 import BeautifulSoup as bs
import requests

HEADERS = {
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 YaBrowser/20.7.0.894 Yowser/2.5 Safari/537.36"
}
# response = requests.get(URL, headers=HEADERS)
# soup = bs(response.content, 'html.parser')
# items = soup.findAll('figcaption', class_='product_item__content product_item__content--block')

MAX_PAGE = 77
pages = []
for i in range(1, MAX_PAGE + 1):
	pages.append(
		requests.get(f'https://www.domofond.ru/prodazha-uchastkizemli-izhevsk-c2017?Page={i}', headers=HEADERS)
	)
data = []
with open('domofond_parser.txt', 'w', encoding='utf-8') as f:
	for response in pages:
		soup = bs(response.content, 'html.parser')
		items = soup.findAll('a', class_='long-item-card__item___ubItG search-results__itemCardNotFirst___3fei6')
		for el in items:
			response_nested = requests.get(f'https://www.domofond.ru{el["href"]}', headers=HEADERS)
			soup_nested = bs(response_nested.content, 'html.parser')
			items_nested = soup_nested.findAll('div', class_='detail-information__row___29Fu6')
			for el_nested in items_nested:
				params = el_nested.get_text(strip=True).split(':')
				if params[0] == 'Цена' or params[0] == 'Расстояние от центра' or params[0] == 'Площадь':
					data.append({params[0]: params[1]})

			try:
				price = data[2]['Цена']
			except IndexError:
				price = "None"
			try:
				area = data[1]['Площадь']
			except IndexError:
				area = "None"
			try:
				distance = data[0]['Расстояние от центра']
			except IndexError:
				distance = "None"

			data = []
			f.write(f'Площадь: {area}; Расстояние до города: {distance}; Цена: {price}\n')