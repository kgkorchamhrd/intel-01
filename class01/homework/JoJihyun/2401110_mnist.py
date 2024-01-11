import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

mnist = tf.keras.datasets.mnist

(image_train, label_train), (image_test, label_test) = mnist.load_data()

print("Train Image Shape : ", image_train.shape)
print("Train Label : ", label_train, "\n")
print(image_train[0])

num = 20
plt.figure(figsize=(15, 15))

for idx in range(num):
    sp = plt.subplot(5, 5, idx+1)
    plt.imshow(image_train[idx], cmap='plasma')
    plt.title(f'Label: {label_train[idx]}')
    plt.xticks([])
    plt.yticks([])
plt.tight_layout()
plt.show()

model = tf.keras.Sequential()
model.add(tf.keras.Input(shape=(28, 28)))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation='sigmoid'))
model.add(tf.keras.layers.Dense(64, activation='sigmoid'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'])
model.fit(image_train, label_train, epochs=10, batch_size=10)
model.summary()

predict = model.predict(image_test[0:num])
print(predict)

print("Prediction : ", np.argmax(predict, axis=1))
plt.figure(figsize=(15, 15))

for idx in range(num):
    sp = plt.subplot(5, 5, idx+1)
    plt.imshow(image_test[idx], cmap='plasma')
    plt.title(f'Label: {predict[idx]}')
    plt.xticks([])
    plt.yticks([])
plt.tight_layout()
plt.show()