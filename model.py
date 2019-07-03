import keras
from keras.layers import *
import os

class Model():
    def __init__(self):
        _input = Input((48, 48, 1))
        a = SeparableConv2D(32, (3, 3), padding="same")(_input)
        b = Conv2D(32, (1, 1), padding="same")(_input)
        b = SeparableConv2D(32, (3, 3), padding="same")(b)
        c = Conv2D(32, (1, 1), padding="same")(_input)
        c = SeparableConv2D(32, (7, 7), padding="same")(c)
        c = SeparableConv2D(32, (3, 3), padding="same")(c)
        x = Concatenate()([a, b, c])
        x = BatchNormalization(axis=-1)(x)
        x = ReLU(6.0)(x)
        x = MaxPooling2D((3,3), strides=(2,2), padding="same")(x)
        x = Dropout(0.25)(x)
        residual = Conv2D(192, (1,1), strides=(2,2), padding="same")(x)
        residual = BatchNormalization(axis=-1)(residual)

        a = SeparableConv2D(64, (3, 3), padding="same")(x)
        b = Conv2D(64, (1, 1), padding="same")(x)
        b = SeparableConv2D(64, (3, 3), padding="same")(b)
        c = Conv2D(64, (1, 1), padding="same")(x)
        c = SeparableConv2D(64, (7, 7), padding="same")(c)
        c = SeparableConv2D(64, (3, 3), padding="same")(c)
        x = Concatenate()([a, b, c])
        x = BatchNormalization(axis=-1)(x)
        x = ReLU(6.0)(x)
        x = MaxPooling2D((3,3), strides=(2,2), padding="same")(x)
        x = Add()([x, residual])
        x = Dropout(0.25)(x)
        residual = Conv2D(256, (1,1), strides=(2,2), padding="same")(x)
        residual = BatchNormalization(axis=-1)(residual)

        a = SeparableConv2D(128, (3, 3), padding="same")(x)
        b = Conv2D(128, (1, 1), padding="same")(x)
        b = SeparableConv2D(128, (3, 3), padding="same")(b)
        x = Concatenate()([a, b])
        x = BatchNormalization(axis=-1)(x)
        x = ReLU(6.0)(x)
        x = MaxPooling2D((3, 3), strides=(2, 2), padding="same")(x)
        x = Add()([x, residual])
        x = Dropout(0.25)(x)

        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.25)(x)
        x = Dense(256)(x)

        output = Dense(310, activation="sigmoid")(x)

        self.model = keras.Model(inputs=_input, outputs=output)
        self.model.summary()
        self.model.compile(optimizer=keras.optimizers.Adam(0.0004), loss='binary_crossentropy',
              metrics=["acc", "mse"])
        if(self.load_weights()):
            print("weights loaded!")
    def load_weights(self, path="model.h5"):
        if os.path.isfile(path):
            try:
                self.model.load_weights(path)
                return True
            except:
                pass
        return False
if __name__ == "__main__":
    model=Model ()
    mod = model.model