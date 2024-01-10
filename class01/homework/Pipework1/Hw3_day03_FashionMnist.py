#handwriten digit
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Flatten, Dense
import matplotlib.pyplot as plt
import numpy as np


mnist = tf.keras.datasets.fashion_mnist
(image_train, label_train), (image_test, label_test) = mnist.load_data()

print("Train Image shape : ", image_train.shape)

print("Train Label : ", label_train, "\n")

print(image_train[0])



NUM=20
plt.figure(figsize=(15,15))
for idx in range(NUM):
    sp = plt.subplot(5,5, idx+1)
    plt.imshow(image_train[idx])
    plt.title(f'Label: {label_train[idx]}')
plt.show()



model = tf.keras.Sequential()

model.add(tf.keras.Input(shape=(28, 28)))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(512, activation='sigmoid'))
model.add(tf.keras.layers.Dense(256, activation='sigmoid'))
model.add(tf.keras.layers.Dense(128, activation='sigmoid'))
model.add(tf.keras.layers.Dense(64, activation='sigmoid'))
model.add(tf.keras.layers.Dense(64, activation='sigmoid'))
model.add(tf.keras.layers.Dense(32, activation='sigmoid'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))



model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

model.fit(image_train, label_train, epochs=10, batch_size=10)

model.summary()



predict = model.predict(image_test)
print(predict[10])
print(np.argmax(predict[10]))


plt.imshow(image_train[10])
plt.title(f'Label: {label_train[10]}')
plt.show()