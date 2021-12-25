from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from dao import PhotoDAO, WorkDAO 
from model import Model
import requests
import base64
import os
import json
from util import getConnect
import error


class Service:
	def createTemp(self, extension, imgCode):
		temp = 'temp.' + extension
		open(temp, 'wb').write(imgCode)
		img = load_img(temp, target_size=(224,224))
		if os.path.isfile(temp):
			os.remove(temp)

		return img


	def predict(self, newModel, image, isLabeling):
		preds = decode_predictions(newModel.predict(image), top=50)
		if isLabeling:
			result = [[p[1], str(p[2])] for p in preds[0]]
		else:
			result = [[p[1], p[2]] for p in preds[0]]

		return result


	def decode(self, base64string):
		if "," in str(base64string):
			extension = str(base64string).split(',')[0].split("/")[1].split(";")[0]
			base64string = str(base64string).split(',')[1]
		else: 
			extension = "jpg"
		decoded = base64.b64decode(base64string)
		img = self.createTemp(extension, decoded)
		return img


	def preprocessing(self, img):
		img_array = img_to_array(img)
		img_array = np.expand_dims(img_array, axis=0)
		img_array = preprocess_input(img_array)

		return img_array


	def labeling(self):
		photoDAO = PhotoDAO()
		result = False
		newModel = Model().loadModel()

		try:
			conn = getConnect()
			cur = conn.cursor()
			dtoList = photoDAO.findAllUnlabeled(cur)
			for dto in dtoList:
				url = dto.getStoredFilePath()
				if dto.getLabel() is None:
					res = requests.get(url)
					extension = url.split("/")[-1].split(".")[1]

					img = self.createTemp(extension, res.content)
					preprocessedImg = self.preprocessing(img)
					preds = self.predict(newModel, preprocessedImg, True)

					label = json.dumps({"data": preds})
					result = photoDAO.updateLabel((label, dto.getPhotoIdx()),conn,cur)
		except Exception as e:
			print(error.connection)
			print(e) 			
		finally:
			if conn:
				conn.close()
			if cur:
				cur.close() 

		return result


	def search(self, base64string):
		analyzed = {}
		newModel = Model().loadModel()
		decoded = self.decode(base64string)
		preprocessedImage = self.preprocessing(decoded)
		preds = self.predict(newModel, preprocessedImage, False)

		dtoList = PhotoDAO().findAllLabeled()
		for dto in dtoList:
			key = dto.getPhotoIdx()
			value = [dto.getWorkIdx(), 0, dto.getStoredFilePath()]

			analyzed.setdefault(key, value) # 추천리스트에 이미지 idx 등록
			for label in dto.getLabel():
				for predict in preds:
					if label[0] == predict[0]:
						analyzed[key][1] += (float(label[1])*float(predict[1])*1000) # 키워드의 정확도 합산
						break
		seacrhResult = self.rank(analyzed)

		return seacrhResult


	def rank(self, analyzed):
		rankList = []
		sortedList = sorted(analyzed.items(), key=lambda x: x[1][1], reverse=True)[:5]
		try:
			conn = getConnect()
			cur = conn.cursor()
			for i in range(len(sortedList)):
				ranked = {
										"rank" : i+1, 
										"photoIdx" : sortedList[i][0], 
										"workIdx" : sortedList[i][1][0],
										# "photographerIdx" : WorkDAO().findPhotographerIdx(sortedList[i][1][0],cur), 
										"storedFilePath" : sortedList[i][1][2]
									}
				rankList.append(ranked)
		except Exception as e:
			print(error.connection)
			print(e) 			
		finally:
			if conn:
				conn.close()
			if cur:
				cur.close() 

		return rankList

if __name__ == "__main__":
	Service().labeling()