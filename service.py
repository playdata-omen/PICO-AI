import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array

import model 

from tensorflow import keras
from scipy import ndimage
import base64

# from tf.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
# from tf.keras.preprocessing.image import load_img, img_to_array

model = model.Model()

class Service():
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    train_images = train_images / 255.0
    test_images = test_images / 255.0
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
            'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    picture = load_img('test.jpg', target_size=(224,224))
    picture_name = 'test1'

    def train_test():
        # new_model = model.Model.load_model()

        new_model = tf.keras.models.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation='relu'),
            # keras.layers.Dropout(0.2),
            keras.layers.Dense(10)
        ])
        new_model.compile(optimizer='adam',
                        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                        metrics=['accuracy'])

        # 모델의 가중치를 저장하는 콜백 만들기
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=model.Model.checkpoint_path,
                                                        save_weights_only=True,
                                                        verbose=1,
                                                        period=10)
        # 새로운 콜백으로 모델 훈련하기
        new_model.fit(Service.train_images, 
                Service.train_labels,  
                epochs=10,
                validation_data=(Service.test_images, Service.test_labels),
                callbacks=[cp_callback],
                verbose=1)
        print("학습 완료")


    def evaluate(new_model):
        test_loss, test_acc = new_model.evaluate(Service.test_images, Service.test_labels, verbose=2)
        print("평가 완료")


    def predict_test(new_model, index):
        probability_model = tf.keras.Sequential([new_model, tf.keras.layers.Softmax()])
        predictions = probability_model.predict(Service.test_images)
        # print(predictions[index])
        # print(np.argmax(predictions[0]))
        # print(Service.test_labels[0])

        print("예측 완료")

        return predictions

    
    def predict(new_model, picture):
        probability_model = tf.keras.Sequential([new_model, tf.keras.layers.Softmax()])
        prediction = probability_model.predict(picture)

        return prediction


    def graph_test(new_model):
        def plot_image(i, predictions_array, true_label, img):
            true_label, img = true_label[i], img[i]
            plt.grid(False)
            plt.xticks([])
            plt.yticks([])

            plt.imshow(img, cmap=plt.cm.binary)

            predicted_label = np.argmax(predictions_array)
            if predicted_label == true_label:
                color = 'blue'
            else:
                color = 'red'

            plt.xlabel("{} {:2.0f}% ({})".format(Service.class_names[predicted_label],
                                            100*np.max(predictions_array),
                                            Service.class_names[true_label]),
                                            color=color)

        def plot_value_array(i, predictions_array, true_label):
            true_label = true_label[i]
            plt.grid(False)
            plt.xticks(range(10))
            plt.yticks([])
            thisplot = plt.bar(range(10), predictions_array, color="#777777")
            plt.ylim([0, 1])
            predicted_label = np.argmax(predictions_array)

            thisplot[predicted_label].set_color('red')
            thisplot[true_label].set_color('blue')
        

        # Plot the first X test images, their predicted labels, and the true labels.
        # Color correct predictions in blue and incorrect predictions in red.
        num_rows = 5
        num_cols = 3
        num_images = num_rows*num_cols
        plt.figure(figsize=(2*2*num_cols, 2*num_rows))
        for i in range(num_images):
            predictions = Service.predict_test(new_model, i)

            plt.subplot(num_rows, 2*num_cols, 2*i+1)
            plot_image(i, predictions[i], Service.test_labels, Service.test_images)
            
            plt.subplot(num_rows, 2*num_cols, 2*i+2)
            plot_value_array(i, predictions[i], Service.test_labels)
        plt.tight_layout()
        plt.show()


    def search(preprocessed_image):
        # # imagenet에 미리 훈련된 ResNet50 모델 불러오기
        model = ResNet50(weights='imagenet')
        # model.summary()
        
        # # # 테스트할 이미지 불러오기
        # img_path = 'test2.jpg'
        # img = load_img(img_path, target_size=(224, 224)) 
        
        # # # ResNet에 입력하기 전에 이미지 전처리
        # x = img_to_array(preprocessed_image)
        # x = np.expand_dims(x, axis=0)

        # x = preprocess_input(x)
        
        # # # # 이미지 분류
        # preds = model.predict(x)
        # print('Predicted:', decode_predictions(preds, top=5)[0])
        
        # # 이미지 분류
        preprocessed_image = preprocess_input(preprocessed_image) # 전처리 입력

        preds = model.predict(preprocessed_image)
        results = decode_predictions(preds, top=10)
        print(results)

        return results[0]


    def decode(self, base64_string):
        image = base64.b64decode(base64_string)
        return image


    def preprocessing(self, image):
        img_array = img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        img_array = img_array / 255.0

        return img_array


    def labeling(self, datas):
        model = ResNet50(weights='imagenet')
        result = False
        
        for i in range(len(datas)):
            preds = decode_predictions(model.predict(datas[i][1]), top=10)
            datas[i][2] = [p[1] for p in preds[0]]
            
        print(datas)

        # DB에 라벨 업데이트 추가하기
        result = True

        return result


    def train(self, images, labels):
        print(type(images[0]))
        result = False
        new_model = model.load_model()
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=model.checkpoint_path,
                                                        save_weights_only=True,
                                                        verbose=1,
                                                        period=10)
        new_model.fit(images, 
                labels,  
                epochs=10,
                validation_data=(Service.test_images, Service.test_labels),
                callbacks=[cp_callback],
                verbose=1)

        result = True

        return result


if __name__ == "__main__":
    # print(Service.train_images)
    # print(type(Service.train_images))

    images = []
    images.append(load_img('test3.jpg', target_size=(224,224)))
    images.append(load_img('test4.jpg', target_size=(224,224)))

    # print(type(images))
    # print(images)

    # img_array = img_to_array(images)
    # img_array = np.expand_dims(img_array, axis=0)
    # img_array = preprocess_input(img_array)
    # img_array = img_array / 255.0
        
    # img_array = Service().preprocessing(images)

    # print(img_array[0])
    # print(type(img_array))
    # print(type(img_array[0]))

    Service().labeling(images)

    # new_model = model.Model.load_model()
    # Service.train_test()
    # Service.evaluate(new_model)
    # Service.predict_test(new_model, 0)
    # Service.graph_test(new_model)

    # picture = Service.picture
    
    # print(Service.picture.shape)
    # picture = ndimage.rotate(Service.picture, 270)
    # picture = picture / 255.0
    
    # plt.figure()
    # plt.imshow(picture)
    # plt.colorbar()
    # plt.grid(False)
    # plt.show()

    # with open("test_encode.txt", "rb") as encode:
    #     Service.decode(encode.read())
