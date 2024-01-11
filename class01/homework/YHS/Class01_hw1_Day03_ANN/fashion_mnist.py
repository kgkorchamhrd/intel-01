import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Flatten, Dense
import matplotlib.pyplot as plt
import numpy as np

# handwriten digit
# mnist = tf.keras.datasets.mnist

# fashion mnist
mnist= tf.keras.datasets.fashion_mnist

(image_train, label_train), (image_test, label_test) = mnist.load_data()
print("Train Image shape: ", image_train.shape)
print("Train Label: ",label_train, end='\n')
# print(image_train[0])

# NUM=20
# plt.figure(figsize=(15,15))
# for idx in range(NUM):
#     sp = plt.subplot(5,5,idx+1)
#     plt.imshow(image_train[idx])
#     plt.title(f'Label: {label_train[idx]}')
# plt.show()

# label_train = tf.keras.utils.to_categorical(label_train)

model = Sequential([
    Input(shape=(28,28)),
    Flatten(),
    Dense(512, activation='sigmoid'),
    Dense(256, activation='sigmoid'),
    Dense(128, activation='sigmoid'),
    Dense(64, activation='sigmoid'),
    Dense(32, activation='sigmoid'),
    Dense(10, activation='softmax')
    ], name='Simple-ANN'
)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
model.fit(image_train, label_train, epochs=10, batch_size=10)

predict = model.predict(image_test)
print(predict[10])
print(np.argmax(predict[10]))

plt.imshow(image_test[10])
plt.title(f'Label: {label_test[10]}')
plt.show()
