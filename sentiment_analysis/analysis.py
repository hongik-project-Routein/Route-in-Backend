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


def sentiment_analysis(new_sentence):
    print('원문: ', new_sentence)
    new_sentence = mecab.morphs(new_sentence)  # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords]  # 불용어 제거
    print('토큰화 및 불용어 제거: ', new_sentence)
    encoded = tokenizer.texts_to_sequences([new_sentence])  # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen=max_len)  # 패딩

    score = float(loaded_model.predict(pad_new))  # 예측
    print('점수: ', score)
    print('감정점수: ', 0 if score < 0.5 else 1)
    print()


sentiment_analysis('요트는 처음 타봤는데 너무 시원하고 좋았어요 ㅎㅎ')
sentiment_analysis('신축이라 그런지 시설이 넓고 깨끗했다!')
sentiment_analysis('음 맛있기는 했는데 알바생 태도가 영.. 다시 올 일은 없을듯 ^^')
