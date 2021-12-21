import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.resnet50 import ResNet50

class Model():
    modelPath = 'saved_model/my_model'
    checkpointPath = "saved_model/training_1/cp.ckpt"
    checkpointDir = os.path.dirname(checkpointPath)
    checkpoint = tf.train.latest_checkpoint(checkpointDir) 


    def createModel():
        newModel = tf.keras.models.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation='relu'),
            # keras.layers.Dropout(0.2),
            keras.layers.Dense(10)
        ])
        newModel.compile(optimizer='adam',
                        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                        metrics=['accuracy'])
        # Model.save_model(newModel)
        # newModel.summary()
        # print('생성 및 저장 완료')

        return newModel


    def saveResNetModel(self):
        newModel = ResNet50(weights='imagenet')
        newModel.save(Model.modelPath)
        newModel.summary()
        print('저장 완료')


    def loadModel(self):
        newModel = tf.keras.models.load_model(Model.modelPath)

        return newModel
