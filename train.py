# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
# Helper libraries
import numpy as np
import os
import clarify
import time
import matplotlib.pyplot as plt

print(tf.__version__)

train_folder = 'dataset/train_cl_canny/'
test_folder = 'dataset/test_cl_canny/'

train_list = [a for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"]
len_train_list = len(train_list)
train_dict = dict(zip(range(0, len(train_list)), train_list))
train_dict.update({v: k for k, v in train_dict.items()})

temp_list = [0 for i in range(0, len(train_list) * 5)]
train_images = []
train_labels = []
test_images = []
test_labels = []


def calc_acc(y_true, y_pred):
    return None


print("Loading train images.")
for x in os.listdir(train_folder):
    # get images in train folder
    # label in filename
    label = list(temp_list)
    for index, l in enumerate(x.split("_")[0]):
        label[train_dict[l] + (index * len_train_list)] = 1
    # images have already clarified. so only import them in grayscale mode
    clf = clarify.clarify(train_folder + x, gray=True)
    image = clf.img
    # add 1 dimension in order to fit it in model.
    image = np.expand_dims(image, 2)
    train_labels.append(label)
    train_images.append(image)

print("Loading test images.")
for x in os.listdir(test_folder):
    # get images in test folder
    # label in filename
    label = list(temp_list)
    for index, l in enumerate(x.split("_")[0]):
        label[train_dict[l] + (index * len_train_list)] = 1
    # images have already clarified. so only import them in grayscale mode
    clf = clarify.clarify(test_folder + x, gray=True)
    image = clf.img
    # add 1 dimension in order to fit it in model.
    image = np.expand_dims(image, 2)
    test_labels.append(label)
    test_images.append(image)

img_count = len(train_images)
train_images = np.array(train_images)
train_labels = np.array(train_labels)
test_images = np.array(test_images)
test_labels = np.array(test_labels)

print("All images have loaded.")
# reduce arrays into 0-1 range
train_images = train_images / 255.0
test_images = test_images / 255.0

if os.path.isfile("model.json") and os.path.isfile("model.h5"):
    # load model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    model = keras.models.model_from_json(loaded_model_json)
    model.load_weights("model.h5")
    print("Loaded model from disk")
else:
    # create model
    model = keras.Sequential()
    # 1_conv
    model.add(keras.layers.Conv2D(32, (3, 3), padding="same",
                                  input_shape=(60, 200, 1)))
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.BatchNormalization(axis=-1))
    model.add(keras.layers.MaxPooling2D(pool_size=(3, 3)))
    model.add(keras.layers.Dropout(0.25))
    model.add(keras.layers.Conv2D(64, (3, 3), padding="same"))
    # 2_conv
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.BatchNormalization(axis=-1))
    model.add(keras.layers.Conv2D(64, (3, 3), padding="same"))
    # 3_conv
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.BatchNormalization(axis=-1))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layers.Dropout(0.25))
    model.add(keras.layers.Conv2D(128, (3, 3), padding="same"))
    # 4_conv
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.BatchNormalization(axis=-1))
    model.add(keras.layers.Conv2D(128, (3, 3), padding="same"))
    # 5_conv
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.BatchNormalization(axis=-1))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layers.Dropout(0.25))
    model.add(keras.layers.Flatten())
    # 1 dim
    model.add(keras.layers.Dense(1024))
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(310))
    model.add(keras.layers.Activation("sigmoid"))
    # multi label classifier

model.compile(optimizer=tf.train.AdamOptimizer(0.0004),
              loss='categorical_crossentropy',
              metrics=["acc"])
while True:
    # batch size may depend on hardware
    model.fit(train_images, train_labels, epochs=5, batch_size=int(train_images.shape[0] / 200))
    # save model
    print("Train Completed. Saving Model.")
    model_json = model.to_json()
    timestamp = str(time.time())
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("models/model.h5")
    print("Saved model to disk.")
    # test the test dataset
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('Test accuracy:', test_acc)
    print('Test loss:', test_loss)
