import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# 예시 데이터 (n=5)


def get_model(n: int):
    model = Sequential()
    model.add(Dense(64, input_dim=2, activation='relu'))  # 2개의 특성(input_dim=2)
    model.add(Dense(32, activation='relu'))  # 중간 레이어
    model.add(Dense(1))  # 출력 레이어: n*1 벡터 출력
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 모델 학습
    model.fit(X, y, epochs=100, batch_size=1, verbose=1)

    # 예측 (입력값을 주고 결과 예측)
    predictions = model.predict(X)
    print(predictions)
