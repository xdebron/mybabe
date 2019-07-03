# MyBaBe
MyBB CAPTCHA Solver using Conventional Neural Network in Keras

Original Image:

![tested image](https://raw.githubusercontent.com/xdebron/mybabe/master/test.png)

After Preprocess:

![tested image](https://raw.githubusercontent.com/xdebron/mybabe/master/test_clarified.png)

Guessed:

![output](https://raw.githubusercontent.com/xdebron/mybabe/master/output.png)

## Getting Started

I've uploaded a image in dataset folder so that you can understand better the structure and file naming scheme.

### Dependencies

* Tensorflow(Keras)
* OpenCV
* Python 3
* Php >= 5

### Creating dataset

You must create dataset first with modified version of captcha.php in mybb.

Run it in terminal or in browser.
```
php captcha.php
```

After created about 100k images you can proceed to Training.


### Training

Just run train.py

```
python3 train.py
```

### Usage

I have also provided pre-trained model so you can directly use it. Also you can include it in your projects easily.

```
python3 eval.py
```
Evaluates test.png. Outputs like this:
```
{'h': 0.95185363, '4': 0.3711427, '5': 0.8917278, 'w': 0.98471284, 'l': 0.86197835}
h45wl
```