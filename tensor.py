from __future__ import absolute_import, division, print_function, unicode_literals
from additional_data import get_train_data
from tensorflow import keras
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
import tensorflow as tf

# На обучение 13000 данных, на проверку 2000 данных
(train_data, train_price), (test_data, test_price) = get_train_data(end=13000), get_train_data(start=13000)


def set_data_from_design(data, price):
    global train_data, train_price
    train_data, train_price = data, price


def create_model():
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

    return model


model = create_model()
# early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)

checkpoint_weights = "training/cp.ckpt"

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_weights,
                                                 save_weights_only=True,
                                                 verbose=1)

model.fit(x=train_data, y=train_price,
          validation_data=(test_data, test_price),
          callbacks=[cp_callback],
          batch_size=128, epochs=3000)

test_loss, test_acc = model.evaluate(test_data, test_price, verbose=2)

print('\nТочность на проверочных данных:', test_acc)

print('\n\n\n')
print(float(model.predict([[23, 31, 3.0, 3.0, 2.9, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]])) * 6 * 10 ** 9)
