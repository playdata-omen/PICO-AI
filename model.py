import os

import tensorflow as tf
from tensorflow import keras

class Model():
    model_path = 'saved_model/my_model'
    checkpoint_path = "saved_model/training_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    checkpoint = tf.train.latest_checkpoint(checkpoint_dir) # 최근 5개의 체크포인트 중, 가장 최근 것으로 설정

    # 간단한 Sequential 모델을 정의합니다
    def create_model():
        new_model = tf.keras.models.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation='relu'),
            # keras.layers.Dropout(0.2),
            keras.layers.Dense(10)
        ])
        new_model.compile(optimizer='adam',
                        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                        metrics=['accuracy'])
        # Model.save_model(new_model)
        # new_model.summary()
        # print('생성 및 저장 완료')

        return new_model


    # 모델구조+가중치 합쳐서 저장하는 방식 -> 재학습이 불가능
    # 가중치만 저장하는 방식은 재학습 가능 
    # def save_model(model): 
    #     model.save(Model.model_path)
    #     model.summary()
    #     print('저장 완료')


    # 현재 방식은 불러올 때마다 모델구조를 새로 생성하고, 가중치만 불러오는 방식
    def load_model(self):
        new_model = Model.create_model() 
        
        if Model.checkpoint is not None:
            new_model.load_weights(Model.checkpoint)
        new_model.summary()
        print('로드 완료')

        return new_model


if __name__ == "__main__":
    # model = Model.create_model()
    # Model.load_model(Model.model_path)



    print(type(Model.checkpoint))