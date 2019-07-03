# Keras
import keras
from keras.layers import *
# Helper libraries
import numpy as np
import os
import clarify
import time
from sklearn.model_selection import train_test_split
import model
import pickle
import matplotlib.pyplot as plt

dataset_folder = 'dataset'

train_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
len_train_list = len(train_list)
train_dict = dict(zip(range(len_train_list), train_list))
train_dict.update({v: k for k, v in train_dict.items()})

temp_list = [0 for i in range(0, len(train_list) * 5)]
print("Loading train images.")
if os.path.isfile("images.bin") and os.path.isfile("labels.bin"):
    with open("images.bin",'rb') as file:
        images = pickle.load(file)
    with open("labels.bin",'rb') as file:
        labels = pickle.load(file)
else:
    images = []
    labels = []
    for x in os.listdir(dataset_folder):
        # get images in train folder
        # label in filename
        label = list(temp_list)
        for index, l in enumerate(x.split("_")[0]):
            label[train_dict[l] + (index * len_train_list)] = 1
        # clarify image
        clf = clarify.clarify(os.path.join(dataset_folder, x))
        clf.clarify_and_gray()
        image = clf.img
        labels.append(label)
        images.append(image)

    images = np.expand_dims(np.array(images), 3)
    labels = np.array(labels)
    with open("images.bin",'wb') as file:
        pickle.dump(images, file)
    with open("labels.bin",'wb') as file:
        pickle.dump(labels, file)

print("All images have loaded.")
# reduce arrays into 0-1 range
images = images / 255.0
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.05, random_state=1337)
del images
del labels

model_class = model.Model()
Model = model_class.model
tb = keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0,
          write_graph=True, write_grads=True, write_images=True)
checkpoint = keras.callbacks.ModelCheckpoint("model.h5", monitor='val_mean_squared_error', verbose=1, save_best_only=True, mode='min')
reduceLROnPlat = keras.callbacks.ReduceLROnPlateau(monitor='val_mean_squared_error', factor=0.1,
                                   patience=10, verbose=1, mode='min', cooldown=2, min_lr=0.000000001,)

# batch size may depend on hardware
Model.fit(train_images, train_labels, epochs=10000, batch_size=256, validation_data=(test_images, test_labels), callbacks=[tb, checkpoint, reduceLROnPlat])
# save model
print("Train Completed. Saving Model.")