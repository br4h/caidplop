from __future__ import absolute_import, division, print_function, unicode_literals
from additional_data import get_train_data
from tensorflow import keras

# На обучение 13000 данных, на проверку 2000 данных
(train_data, train_price), (test_data, test_price) = get_train_data(end=13000), get_train_data(start=13000)


def set_data_from_design(data, price):
    global train_data, train_price
    train_data, train_price = data, price


model = keras.models.Sequential([
    keras.layers.Dense(12, activation='relu'),  # или tanh
    keras.layers.Dropout(0.5),
    keras.layers.Dense(25, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(10, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(1)
])

model.compile(optimizer='adam',
              loss='mse',
              metrics=['accuracy'])

model.fit(x=train_data, y=train_price,
          validation_data=(test_data, test_price),
          batch_size=128, epochs=500)

test_loss, test_acc = model.evaluate(test_data,  test_price, verbose=2)

print('\nТочность на проверочных данных:', test_acc)
