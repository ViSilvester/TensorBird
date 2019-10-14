from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
from pathlib import Path
import os
import random
from tensorflow import keras
import game

PATH = "c:/users/vineo/DEV/tensor bird"

SCREENWIDTH  = int(288/2)
SCREENHEIGHT = int(512/2)
'''
x = np.load(PATH+"/album.npy")
y = np.load(PATH+"/labels.npy")

x = x.reshape(-1,SCREENWIDTH, SCREENHEIGHT, 1)
y = y.reshape(-1, 1)

x = x/255.0
'''
model = keras.Sequential()
model.add(keras.layers.Conv2D(64, (2,2)))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))

model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(64, activation = tf.nn.relu))
model.add(keras.layers.Dense(1 , activation = tf.nn.sigmoid))

model.compile(optimizer = 'adam', loss='binary_crossentropy', metrics =['accuracy'])

cp_callback = tf.keras.callbacks.ModelCheckpoint(PATH+"/pesos.ckpt", save_weights_only= True, verbose =1)

model.load_weights(PATH+"/pesos.ckpt")
#model.fit(x, y, epochs=5, callbacks = [cp_callback])

game.game(model, False, True)