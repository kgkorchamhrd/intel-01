import tensorflow as tf
from tensorflow.keras import datasets, layers, models, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, Flatten, Dense, Input, BatchNormalization, Concatenate, Dropout
import numpy as np
import matplotlib.pyplot as plt
import cv2

model = tf.keras.models.load_model('./GoogleNet_Mnist.h5')
fashion_mnist = tf.keras.datasets.fashion_mnist
(f_image_train, f_label_train), (f_image_test, f_label_test) = fashion_mnist.load_data()

f_image_train, f_image_test = f_image_train / 255, f_image_test / 255

f_image_train = tf.expand_dims(f_image_train, axis=3, name=None)
f_image_test = tf.expand_dims(f_image_test, axis=3, name=None)
f_image_train = tf.repeat(f_image_train, 3, axis=3)
f_image_test = tf.repeat(f_image_test, 3, axis=3, name=None)

num = 10
predict = model.predict(f_image_train[:num])
print(f_label_train[:num])
print("Prediction, ", np.argmax(predict, axis=1))