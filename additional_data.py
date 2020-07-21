def get_train_data(filename='moskow_results', start=0):
    data, price = [], []
    with open(f'{filename}.txt', 'r', encoding='utf8') as f:
        for line in f.readlines()[start:]:
            all_data = line.split(';')[:-1]
            data.append([x.split(':')[1] for x in all_data])
            price.append(all_data[2].split(':')[1])
    return data, price


def get_average(filename='MOSCOW_PARSER'):
    average = [0 for i in range(9)]
    amount = 1  # 7268
    with open(f'{filename}.txt', 'r', encoding='utf-8') as f:
        for i in f:
            amount += 1
            dictionary = list(map(float, [x.split(':')[1].replace(',', '.') for x in i.split(';')[3:-1]]))
            for j in range(9):
                average[j] += dictionary[j]
        for i in range(len(average)):
            average[i] = round(average[i] / amount, 1)
    with open('average_values.txt', 'w', encoding='utf-8') as f:
        f.write(','.join(list(map(str, average))))


def get_average_from_file():
    with open('average_values.txt', 'r') as f:
        return f.read()

