from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import dao, model
import requests
import base64
import os
import json


model = model.Model()
dao = dao.PhotoDAO()

class Service():
	def createTemp(self, extension, imgCode):
		temp = 'temp.' + extension
		open(temp, 'wb').write(imgCode)
		img = load_img(temp, target_size=(224,224))
		if os.path.isfile(temp):
			os.remove(temp)

		return img


	def predict(self, newModel, image, isLabeling):
		# probability_model = tf.keras.Sequential([newModel, tf.keras.layers.Softmax()])
		preds = decode_predictions(newModel.predict(image), top=50)
		if isLabeling:
			result = [[p[1], str(p[2])] for p in preds[0]]
		else:
			result = [[p[1], p[2]] for p in preds[0]]

		return result


	def decode(self, base64_string):
		if ',' in base64_string:
			extension = base64_string.split(',')[0].split("/")[1].split(";")[0]
			base64_string = base64_string.split(',')[1]
		decoded = base64.b64decode(base64_string)
		Service().createTemp(extension, decoded)

		return load_img('temp.jpg', target_size=(224,224))


	def preprocessing(self, img):
		img_array = img_to_array(img)
		img_array = np.expand_dims(img_array, axis=0)
		img_array = preprocess_input(img_array)

		return img_array


	def labeling(self):
		result = False
		dtoList = dao.findAllUnlabeled()
		newModel = model.loadModel()
		for dto in dtoList:
			url = dto.getStoredFilePath()
			if dto.getLabel() is None:
				res = requests.get(url)
				extension = url.split("/")[-1].split(".")[1]

				img = Service().createTemp(extension, res.content)
				preprocessedImg = Service().preprocessing(img)
				preds = Service().predict(newModel, preprocessedImg, True)

				label = json.dumps({"data": preds})
				result = dao.updateLabel((label, dto.getPhotoIdx()))

		return result


	def search(self, base64string):
			recommendList = {}
			newModel = model.loadModel()
			decoded = Service().decode(base64string)
			preprocessedImage = Service().preprocessing(decoded)
			preds = Service().predict(newModel, preprocessedImage, False)

			dtoList = dao.findAllLabeled()

			for dto in dtoList:
				recommendList.setdefault(dto.getPhotoIdx(), [dto.getPhotoIdx(),0]) # 추천리스트에 이미지 idx 등록
				for label in dto.getLabel():
					for predict in preds:
						if label[0] == predict[0]:
							recommendList[dto.getPhotoIdx()][1] += (float(label[1])*float(predict[1])*1000) # 키워드의 정확도 합산
							break
				recommendList[dto.getPhotoIdx()][1] = str(recommendList[dto.getPhotoIdx()][1])

			return recommendList


if __name__ == "__main__":
	# img = load_img("./test_data/event.jpg", target_size=(224,224))
	# result = Service().searchTest(img)
	# print(result)
	
	Service().labeling()