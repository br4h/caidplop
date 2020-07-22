from __future__ import absolute_import, division, print_function, unicode_literals
from additional_data import get_train_data
from tensorflow import keras

# На обучение 13000 данных, на проверку 2000 данных
(train_data, train_price), (test_data, test_price) = get_train_data(), get_train_data(start=13000)


def set_data_from_design(data, price):
    global train_data, train_price
    train_data, train_price = data, price


model = keras.models.Sequential([
    keras.layers.Dense(128, activation='elu'),
    keras.layers.Dense(1)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_data, train_price, epochs=10)
