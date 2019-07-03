import cv2
import numpy as np


class clarify():

    def __init__(self, path=None, img=None):
        # open file into image array or use image itself
        if img is None:
            if path is not None:
                self.img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            else:
                raise Exception('You have to provide a path or image itself.')
        else:
            self.img = img

    # clear image.
    # mybb captcha.php seems make its color palette of string between 0 and 200.
    # anything above 200 is noise.
    # also completely black pixels in edges must filtered
    def clarify_img(self):
        self.img[np.logical_or(np.max(self.img, axis=2)>200, np.sum(self.img, axis=2)==0)] = [255, 255, 255]

    # RGB to GRAY
    def gray(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)

    def resize(self, size):
        self.img = cv2.resize(self.img, size)
    # clear and gray
    def clarify_and_gray(self):
        self.clarify_img()
        self.resize((48, 48))
        self.gray()

if __name__ == "__main__":
    clr = clarify(path="test.png")
    clr.clarify_img()
    clr.gray()
    img = clr.img
    cv2.imwrite("test_clarified.png", img)
    cv2.imshow('clarified', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
