def get_average():
    average = [0 for i in range(9)]
    amount = 1  # 7268
    with open('MOSCOW_PARSER.txt', 'r', encoding='utf-8') as f:
        for i in f:
            amount += 1
            dictionary = list(map(float, [x.split(':')[1].replace(',', '.') for x in i.split(';')[3:-1]]))
            for j in range(9):
                average[j] += dictionary[j]
        for i in range(len(average)):
            average[i] = round(average[i] / amount, 1)
    with open('average_values.txt', 'w', encoding='utf-8') as f:
        f.write(','.join(list(map(str, average))))


if __name__ == "__main__":
    get_average()
