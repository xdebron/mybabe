import numpy as np
import clarify
import os
import cv2
import queue
import threading
import multiprocessing
import time


im_q = queue.Queue()
suffix = "_cl_canny/"

try:
    os.mkdir("dataset/train" + suffix)
    os.mkdir("dataset/test" + suffix)
except:
    None


def saver(path, file):
    clf = clarify.clarify(path + file)
    clf.clarify_and_canny()
    image = clf.img
    cv2.imwrite(path[:-1] + suffix + file, image)


def worker():
    while True:
        data = im_q.get()
        saver(data[0], data[1])


for i in range(0, multiprocessing.cpu_count()):
    threading.Thread(target=worker).start()

for x in os.listdir('dataset/train'):
    im_q.put(["dataset/train/", x])

for x in os.listdir('dataset/test'):
    im_q.put(["dataset/test/", x])

while not im_q.empty():
    print(im_q.qsize())
    time.sleep(1)
