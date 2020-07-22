import re


def get_train_data(filename='results/moscow_results', start=0):
    data, price = [], []
    with open(f'{filename}.txt', 'r', encoding='utf8') as f:
        for line in f.readlines()[start:]:
            all_data = line.split(';')[:-1]
            if ',' in all_data[1]:
                all_data[1] = all_data[1].split(',')[0]
            not_converted = [x.split(':')[1].replace(' ', '').replace(',', '.')
                             for x in all_data
                             if all_data.index(x) != 2]
            to_append = []
            for i in range(len(not_converted)):
                to_append.append(float(not_converted[i])
                                 if '.' in not_converted[i]
                                 else int(re.sub(r'[А-я]', '', not_converted[i].replace('Вчертегорода', '0'))))
            data.append(to_append)
            land_price = int(all_data[2].split(':')[1])
            # print(round(float(land_price / get_maximum()), 8))
            price.append(round(land_price / get_maximum(), 4) if land_price < get_maximum() else 0.9)
    return data, price


def get_average(filename='MOSCOW_PARSER'):
    data = [
        'Эколгоия',
        'Чистота',
        'ЖКХ',
        'Соседи',
        'Условия для детей',
        'Спорт и отдых',
        'Магазины',
        'Транспорт',
        'Безопасность',
        'Уровень жизни'
    ]
    average = [0 for i in range(9)]
    amount = 1
    with open(f'{filename}.txt', 'r', encoding='utf-8') as f:
        for i in f:
            amount += 1
            dictionary = list(map(float, [x.split(':')[1].replace(',', '.') for x in i.split(';')[3:-1]]))
            for j in range(9):
                average[j] += dictionary[j]
        for i in range(len(average)):
            average[i] = round(average[i] / amount, 1)
            average[i] = f'{data[i]}: {average[i]}'
        print(average)
    with open('average_values.txt', 'w', encoding='utf-8') as f:
        f.write(';'.join(list(map(str, average))))


def get_average_from_file():
    with open('average_values.txt', 'r', encoding='utf-8') as f:
        return f.read()


def get_maximum():
    maximum = 0
    try:
        with open('results/maximum.txt', 'r') as f:
            return int(f.readline())
    except FileNotFoundError:
        with open('results/moscow_results.txt', 'r', encoding='utf-8') as f:
            for elem in f.readlines():
                current = int(elem.split(';')[2].split(':')[1])
                if current > maximum:
                    maximum = current
        with open('results/maximum.txt', 'w', encoding='utf-8') as f:
            f.write(str(maximum))
        return maximum
