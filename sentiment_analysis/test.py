import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# 경고 뜨지 않게 설정
import warnings
# 데이터 전처리 알고리즘
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# 학습용/검증용 나누는 함수
from sklearn.model_selection import train_test_split

# 교차 검증

# 지표를 하나만 설정할 경우
from sklearn.model_selection import cross_val_score
# 지표를 하나 이상 설정할 경우
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold

# 모델의 최적의 하이퍼파라미터를 찾기 위한 도구
from sklearn.model_selection import GridSearchCV

# 평가함수

# 분류용
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

# 회귀용
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

# 머신러닝 알고리즘 - 분류
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
# from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier

# 머신러닝 알고리즘 - 회귀
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
# from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import VotingRegressor

# 차원축소
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# 군집화
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth

# ARIMA (시계열 예측)
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm

# 시간 측정을 위한 시간 모듈
import datetime

# 주식정보
# from pandas_datareader import data

# 형태소 벡터를 생성하기 위한 라이브러리
from sklearn.feature_extraction.text import CountVectorizer
# 형태소 벡터를 학습 벡터로 변환
from sklearn.feature_extraction.text import TfidfTransformer

# 데이터 수집
import requests
from bs4 import BeautifulSoup
import re
import time
import os
import json

# 한국어 형태소 분석
from konlpy.tag import Okt, Hannanum, Kkma, Mecab, Komoran

# 워드 클라우드를 위한 라이브러리
from collections import Counter
# import pytagcloud
from IPython.display import Image

# 저장
import pickle

from keras import models
from tensorflow.keras.layers import Embedding, Dense, LSTM, GRU, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfTransformer
import urllib.request

warnings.filterwarnings('ignore')

# 그래프 설정
# plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['font.size'] = 14
plt.rcParams['figure.figsize'] = 12, 8
plt.rcParams['axes.unicode_minus'] = False

'''
From here
'''
df1 = pd.read_csv('../data/naver_dining_review.csv')
df2 = pd.read_csv('../data/ds01.csv')

def text_cleansing(text):
    re_text = re.compile('[^ ㄱ-ㅣ가-힣]+')
    # 지정한 정규식에 해당하지 않은 것은 길이가 0인 문자열로 변환
    res = re_text.sub('', text)
    return res


'''
데이터셋 전처리
'''
# 첫번째 데이터셋(ds01) 전처리
df1["clean_review"] = df1["review"].apply(lambda x: text_cleansing(x))
df1.drop("review", axis=1, inplace=True)
df1['sentiment_score'] = df1['score'].apply(lambda x: 0 if x <= 3 else 1)  # 리뷰점수 3 이하는 부정(0)으로, 4이상은 긍정(1)
df1 = df1[['clean_review', 'sentiment_score']]

# 두번째 데이터셋(naver_dining_review) 전처리
df2["clean_review"] = df2["origin_reivew"].apply(lambda x: text_cleansing(x))
df2.drop("origin_reivew", axis=1, inplace=True)
df2.rename(columns={"sentiment_int": "sentiment_score"}, inplace=True)
df2 = df2[['clean_review', 'sentiment_score']]

# 세번째 데이터셋(naver_shopping) 전처리
urllib.request.urlretrieve("https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt", filename="../data/shop_rating.txt")
shop_df = pd.read_table('../data/shop_rating.txt', names=['ratings', 'origin_reivew'])
shop_df.drop_duplicates(subset=['origin_reivew'], inplace=True) # 중복제거
shop_df["clean_review"] = shop_df["origin_reivew"].apply(lambda x : text_cleansing(x))
shop_df.drop("origin_reivew", axis=1, inplace=True)
shop_df['sentiment_score'] = shop_df['ratings'].apply(lambda x: 0 if x <= 3 else 1) # 리뷰점수 3 이하는 부정(0)으로, 4이상은 긍정(1)
shop_df = shop_df[['clean_review', 'sentiment_score']]

# 네번째, 다섯번째 데이터셋(ratings_train, ratings_test) 전처리
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", filename="../data/ratings_train.txt")
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", filename="../data/ratings_test.txt")
movie_df1 = pd.read_table("../data/ratings_train.txt")
movie_df2 = pd.read_table("../data/ratings_test.txt")
movie_df1 = movie_df1.drop(['id'], axis=1)
movie_df2 = movie_df2.drop(['id'], axis=1)
movie_df1.rename(columns = {"document": "clean_review", "label" : "sentiment_score"}, inplace = True)
movie_df2.rename(columns = {"document": "clean_review", "label" : "sentiment_score"}, inplace = True)


'''
데이터셋 합치기
'''
pdList = [df1, df2, shop_df, movie_df1, movie_df2]
all_df = pd.concat(pdList).reset_index(drop=True)
all_df['clean_review'].nunique(), all_df['sentiment_score'].nunique()
all_df.isnull().sum()
all_df.drop_duplicates(subset = ['clean_review'], inplace = True)
# 총 414587개


'''
학습용, 테스트용 데이터셋 분리
'''
train, test = train_test_split(all_df, test_size=0.2, random_state=210617)
print('훈련용 리뷰의 개수 :', len(train))
print('테스트용 리뷰의 개수 :', len(test))
print('-' * 40)

# 학습용 데이터셋 라벨 분포 확인
train['sentiment_score'].value_counts().plot(kind='bar')
print(train.groupby('sentiment_score').size().reset_index(name='count'))
print('-' * 40)


'''
Mecab 분석기로 문장 토크나이징
'''
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지',
             '임', '게']

mecab = Mecab()
tokens = mecab.morphs("하란 교수님 만세")
print('MECAB 형태소 분석: ', tokens)
print('-' * 40)

train_list = []
test_list = []


# train['clean_review'] 에서 결측값 확인 및 처리
if train['clean_review'].isnull().sum() > 0:
    train['clean_review'].fillna('', inplace=True)

for sentence in train['clean_review']:
    temp_X = mecab.morphs(sentence)  # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
    train_list.append(temp_X)

# test['clean_review'] 에서 결측값 확인 및 처리
if test['clean_review'].isnull().sum()> 0:
    test['clean_review'].fillna('', inplace=True)

for sentence in test['clean_review']:
    temp_X = mecab.morphs(sentence)  # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
    test_list.append(temp_X)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_list)
tokenizer.fit_on_texts(test_list)


'''
pickle
'''
# 저장하기
with open("all_reviews.pickle", "wb") as fw:
    pickle.dump(tokenizer, fw)

# # 불러오기
# with open("all_reviews.pickle", "rb") as fr:
#     tokenizer = pickle.load(fr)
# train_list = []
# test_list = []
# tokenizer.fit_on_texts(train_list)
# tokenizer.fit_on_texts(test_list)

'''
단어 등장 빈도 수 체크
'''
threshold = 3
total_cnt = len(tokenizer.word_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# key, value == 단어, 빈도수
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

print('단어 집합(vocabulary)의 크기 :', total_cnt)
print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s' % (threshold - 1, rare_cnt))
print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt) * 100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq) * 100)
print('-' * 40)


'''
~
'''
# 단어로 쪼개진 문장 숫자로 변환
t_train1 = tokenizer.texts_to_sequences(train_list)
t_test1 = tokenizer.texts_to_sequences(test_list)

# 정답으로 사용할 감정점수 분류
s_train = train['sentiment_score']
s_test = test['sentiment_score']

print('문장의 최대 길이 :', max(len(l) for l in t_train1))
print('문장의 평균 길이 :', sum(map(len, t_train1)) / len(t_train1))
print('-' * 40)

# 히스토그램이 잘 출력이 안됨 WTF
plt.hist([len(s) for s in t_train1], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()


'''
문장 패딩
'''
def below_threshold_len(max_len, nested_list):
    cnt = 0
    for s in nested_list:
        if (len(s) <= max_len):
            cnt = cnt + 1
    print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s' % (max_len, (cnt / len(nested_list)) * 100))
    print('-' * 40)

max_len = 54
below_threshold_len(max_len, t_train1)
# 전체 샘플 중 길이가 54 이하인 샘플의 비율: 99.31456945532915
# 길이를 길게 잡을 경우 학습에 시간이 오래걸리기 때문에, 가장 데이터손실이 적으면서도 학습시간을 줄일 수 있도록
# 전체의 99.31%를 포함하도록 문장길이를 54로 설정했음

t_train2 = pad_sequences(t_train1, maxlen=max_len)
t_test2 = pad_sequences(t_test1, maxlen=max_len)


'''
Sequential 모델 생성
'''

model = Sequential()
vocab_size = total_cnt + 1
model.add(Embedding(vocab_size, 100))  # 100차원의 임베딩 사용
model.add(LSTM(128, return_sequences=True))  # 레이어 128개의 LSTM 유닛, 시퀀스 예측을 위해 return_sequences=True
model.add(Dropout(0.5))  # 레이어 과적합을 방지하기 위해 50%의 드롭아웃 적용
model.add(GRU(128))  # 레이어 128개의 GRU 유닛 사용
model.add(Dropout(0.5))  # 레이어 과적합을 방지하기 위해 50%의 드롭아웃 적용
model.add(Dense(1, activation='sigmoid'))  # 이진분류를 위한 Dense 레이어 추가, 활성화 함수 sigmoid 사용

# 모델 구조 요약하여 표시
model.summary()

# 검증 손실(val_loss) 모니터링, 손실이 4번 연속으로 개선되지 않으면 학습 중단
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
# 검증 정확도(val_acc) 모니터링, 모델의 최상 가중치 저장
mc = ModelCheckpoint('bilstm2.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)


'''
모델 컴파일
'''
# 옵티마이저, 손실함수, 평가 메트릭 지정
model.compile(optimizer='adam', loss='mse', metrics=['acc'])


'''
모델 훈련
'''
history = model.fit(t_train2, s_train, epochs=2, callbacks=[es, mc], batch_size=6000, validation_split=0.2)


loaded_model = load_model('bilstm2.h5')
print("\n테스트 정확도: %.4f" % (loaded_model.evaluate(t_test2, s_test)[1]))