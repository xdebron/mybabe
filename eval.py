import os
import clarify
import model
import numpy as np

class predictor():
    def __init__(self,debug=False):

        # init vars
        self.debug=debug
        self.train_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")

        # load model
        _model = model.Model()
        self.model = _model.model
    def predict_image(self, path=None, image=None):
        # clarify the image first
        clf = clarify.clarify(img=image,path=path)
        clf.clarify_and_gray()
        image = clf.img / 255.0
        # add dimensions in order to fit it in model
        image = np.expand_dims(image, 2)
        image = np.expand_dims(image, 0)

        # get prediction from model
        prediction = self.model.predict(image)

        # models output is list of prob list. get maximum value of each list of prob list with stride=train_list_len
        prediction = np.reshape(prediction, (5,62))
        maxs = np.argmax(prediction, axis=1)
        probs = np.max(prediction, axis=1)
        locs = [self.train_list[max] for max in maxs]
        print(dict(zip(locs, probs)))
        # string list to one string
        return "".join(locs)

if __name__ == "__main__":
    predictor_=predictor(debug=True)
    print(predictor_.predict_image("test.png"))