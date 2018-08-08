import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
from tensorflow import keras
import clarify
import numpy as np

class predictor():
    def __init__(self,debug=False):

        # init vars
        self.debug=debug
        self.train_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        self.train_list_len=len(self.train_list)
        self.train_dict = dict(zip(range(0, self.train_list_len), self.train_list))
        self.train_dict.update({v: k for k, v in self.train_dict.items()})

        # load model
        if os.path.isfile("model.json") and os.path.isfile("model.h5"):
            json_file = open('model.json', 'r')
            loaded_model_json = json_file.read()
            self.model = keras.models.model_from_json(loaded_model_json)
            self.model.load_weights("model.h5")
            if self.debug:
                print("Loaded model from disk")

            self.model.compile(optimizer=tf.train.AdamOptimizer(0.0004),
                          loss='categorical_crossentropy',
                          metrics=['accuracy'])
        else:
            raise Exception("Model not found.")
    def list_to_label(self, list):
        # num array to string list
        return [self.train_dict[x[0]] for x in list]
    def predict_image(self, path=None, image=None):
        # clarify the image first
        clf = clarify.clarify(img=image,path=path)
        clf.clarify_and_canny()
        image = clf.img / 255.0
        # add dimensions in order to fit it in model
        image = np.expand_dims(image, 2)
        image = np.expand_dims(image, 0)

        # get prediction from model
        prediction = self.model.predict(image)

        # models output is list of prob list. get maximum value of each list of prob list with stride=train_list_len
        locs = [
            [np.argmax(prediction[0][x:x + self.train_list_len]), x + np.argmax(prediction[0][x:x + self.train_list_len])]
            for x in range(0, 310, self.train_list_len)]

        # print probs if needed
        if self.debug:
            print([prediction[0][loc[1]] for loc in locs])
            print(self.list_to_label(locs))

        # string list to one string
        return "".join(self.list_to_label(locs))

if __name__ == "__main__":
    predictor_=predictor(debug=True)
    print(predictor_.predict_image("test.png"))