import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# 학습용 데이터
corpus = [
    "나는 밥을 먹었다",
    "나는 학교에 갔다",
    "나는 책을 읽었다",
    "나는 친구를 만났다",
]

# 토크나이징
tokenizer = Tokenizer()
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1
print(tokenizer.word_index)
# # 시퀀스 생성
# input_sequences = []
# for line in corpus:
#     token_list = tokenizer.texts_to_sequences([line])[0]
#     for i in range(1, len(token_list)):
#         n_gram_sequence = token_list[:i+1]
#         input_sequences.append(n_gram_sequence)

# # 패딩 및 데이터 준비
# max_seq_len = max(len(x) for x in input_sequences)
# input_sequences = pad_sequences(
#     input_sequences, maxlen=max_seq_len, padding='pre')

# xs = input_sequences[:, :-1]
# labels = input_sequences[:, -1]
# ys = to_categorical(labels, num_classes=total_words)

# # 모델 구성
# model = tf.keras.Sequential([
#     tf.keras.layers.Embedding(total_words, 10, input_length=max_seq_len-1),
#     tf.keras.layers.LSTM(100),
#     tf.keras.layers.Dense(total_words, activation='softmax')
# ])

# model.compile(loss='categorical_crossentropy',
#               optimizer='adam', metrics=['accuracy'])
# model.fit(xs, ys, epochs=200, verbose=0)

# # 다음 단어 예측 함수


# def predict_next_word(model, tokenizer, text):
#     token_list = tokenizer.texts_to_sequences([text])[0]
#     token_list = pad_sequences(
#         [token_list], maxlen=max_seq_len-1, padding='pre')
#     predicted = model.predict(token_list, verbose=0)
#     predicted_word_index = np.argmax(predicted)
#     for word, index in tokenizer.word_index.items():
#         if index == predicted_word_index:
#             return word


# # 예측 예시
# print(predict_next_word(model, tokenizer, "나는 밥을"))
