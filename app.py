import json
from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import base64
from PIL import Image
from io import BytesIO

import matplotlib.pyplot as plt

import service


service = service.Service()

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def test():
        return 'test_success'

    @app.route('/test1', methods = ['POST'])
    def test1():
        data = request.get_json()
        return jsonify(data)
    
    @app.route('/test2/<testdata>')
    def test2(testdata):
        return jsonify({"test2data":testdata})


    @app.route('/test3/search_image')
    def test_search_image():
        image = load_img('test.jpg', target_size=(224,224))

        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)

        result = service.Service.search(image_array)
        predicted = result[0][1]
        percentage = str(result[0][2])
        
        return jsonify({"predicted":predicted, "percentage":percentage})


    @app.route('/test4/convert')
    def convert():
        with open('test.jpg', 'rb') as img:     # 이미지 읽어서 base64로 인코딩, txt파일에 저장
            base64_string = base64.b64encode(img.read())

        encoded = open("encode.txt", "wb")
        encoded.write(base64_string)
        encoded.close()

        with open("encode.txt", "rb") as encode:     # base64 읽어서 디코딩, jpg파일에 저장
            decode = base64.b64decode(encode.read())

        decoded = open("decode.jpg", "wb")
        decoded.write(decode)
        decoded.close()

        return "success"


    @app.route('/search_image', methods = ['POST'])
    def search_image():
        image = service.decode(request.get_json())
        result = service.search(image)

        return jsonify({'result' : result})


    # @app.route('/train', methods = ['POST'])
    # def train():
    #     images = []
    #     images.append(load_img('test3.jpg', target_size=(224,224)))
    #     images.append(load_img('test4.jpg', target_size=(224,224)))

    #     preprocessed_images = service.preprocessing(images)
    #     labels = service.labeling(preprocessed_images) 
    #     if service.train(preprocessed_images, labels):
    #         result = '훈련 성공'
    #     else:
    #         result = '훈련 실패'
    #     # 훈련 성공 후, DB에 labels 업데이트 추가하기

    #     return result


    @app.route('/labeling', methods = ['POST'])
    def labeling():
        datas = [[1,'link1',''],[2,'link2','']]
        # S3서버에서 이미지 불러오기 추가하기
        datas[0][1] = load_img('test3.jpg', target_size=(224,224))
        datas[1][1] = load_img('test4.jpg', target_size=(224,224))

        for i in range(len(datas)):
            datas[i][1] = service.preprocessing(datas[i][1])

        if service.labeling(datas):
            result = '라벨링 성공'
        else:
            result = '라벨링 실패'

        return result


    return app

if __name__ == "__main__":
    create_app().run()


