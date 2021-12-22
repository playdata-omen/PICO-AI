import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.resnet50 import ResNet50

class Model():
	modelPath = 'saved_model/my_model'

	def saveResNetModel(self):
		newModel = ResNet50(weights='imagenet')
		newModel.save(Model.modelPath)
		newModel.summary()


	def loadModel(self):
		newModel = tf.keras.models.load_model(self.modelPath)

		return newModel