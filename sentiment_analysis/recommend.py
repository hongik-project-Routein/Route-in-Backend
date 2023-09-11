from tensorflow.keras.models import load_model
import random
from konlpy.tag import Mecab
import os
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

with open("all_reviews.pickle", "rb") as fr:
    tokenizer = pickle.load(fr)

mecab = Mecab()
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']
loaded_model = load_model('bilstm2.h5')
max_len = 54


def recommend_sys(new_sentence):

    print('원문:', new_sentence)
    new_sentence = mecab.morphs(new_sentence)  # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords]  # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence])  # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen=max_len)  # 패딩

    score = float(loaded_model.predict(pad_new))  # 예측
    print('score:', score)
    print()

# while 1:
#     str = input('분석할 문장 입력 >>  ')
#     if not str:
#         break
#
#     recommend_sys(str)
#     print()

recommend_sys('분석할 문장')