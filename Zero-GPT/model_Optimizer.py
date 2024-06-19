import tensorflow as tf
import numpy as np

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(units=3, input_shape=[4]))
model.add(tf.keras.layers.Dense(units=64))
model.add(tf.keras.layers.Dense(units=64))
model.add(tf.keras.layers.Dense(units=64))
model.add(tf.keras.layers.Dense(units=1))

X = [
    
    
    
]