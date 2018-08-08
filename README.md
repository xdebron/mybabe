# MyBaBe
MyBB CAPTCHA Solver using Conventional Neural Network in Keras


## Getting Started

I've uploaded two images dataset folder so that you can understand more better the structure and file naming scheme.

### Dependencies

Tensorflow(I have tried it with 1.9.0)
OpenCV
Python 3

### Creating dataset

You must create dataset first with modified version of captcha.php in mybb.

Run it in terminal or in browser.
...
php captcha.php
...

After created about 100k images you can proceed to step 2. Image clarification.
Your images already present in train and test folders. Just run mass_clarifier.py

...
python3 mass_clarifier.py
...

After it finished you have done with your dataset.

### Training

Just run train.py

...
python3 train.py
...

### Usage

I have also provided pre-trained model so you can directly use it. Also you can include it in your projects easily.

...
python3 eval.py
...

