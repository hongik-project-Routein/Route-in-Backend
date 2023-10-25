import random
import pandas as pd
import statistics
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import operator
from google.cloud import bigquery

from rest_framework.generics import get_object_or_404
from accounts.models import User

def set_table():
    client = bigquery.Client()
    project = "carbon-inkwell-290604"
    dataset_id = "route_in"

    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    table_ref = dataset_ref.table("sentimental_score")
    table = client.get_table(table_ref)

    df = client.list_rows(table).to_dataframe()

    pd_df = df
    pd_df['score'] = pd_df.score.astype(float)
    pd_df.round(5)

    # 테이블 피벗
    pi_pd_df = pd_df.pivot_table(index='userId', columns='mapId', values='score').fillna(0)

    return pi_pd_df


'''
유사한 사용자 찾기
로그인 / 게시글 생성 / (유사한 사용자 추천 시)
'''
def update_sim_users(user_id, k=5):
    matrix = set_table()

    # 현재 유저에 대한 데이터프레임 만들기
    # matrix의 index = user_id -> 현재 1명 유저에 대한 평가 정보 찾기
    user = matrix[matrix.index == user_id]

    if not user.empty:
        # print('(find_similar_user_pd.py:37) user:\n', user)
        # matrix index 값이 user_id와 다른가?
        # 일치하지 않는 값들은 other_users
        other_users = matrix[matrix.index != user_id]
        # print('(find_similar_user_pd.py:42) other_users:\n', other_users)

        # 대상 user, 다른 유저와의 cosine 유사도 계산
        # list 변환
        similarities = cosine_similarity(user, other_users)[0].tolist()

        # 다른 사용자의 인덱스 목록 생성
        other_users_list = other_users.index.tolist()

        # 인덱스/유사도로 이뤄진 딕셔너리 생성
        # dict(zip()) -> {'other_users_list1': similarities, 'other_users_list2': similarities}
        user_similarity = dict(zip(other_users_list, similarities))

        # 딕셔너리 정렬
        # key=operator.itemgetter(1) -> 오름차순 정렬 -> reverse -> 내림차순
        user_similarity_sorted = sorted(user_similarity.items(), key=operator.itemgetter(1), reverse=True)
        print(user_similarity_sorted)

        # 가장 높은 유사도를 가진 유저의 uname k개 정렬
        top_users_similarities = user_similarity_sorted[:k]
        k_users = [i[0] for i in top_users_similarities]
        # print('(find_similar_user_pd.py:63) k_users:', k_users)

        # 실제 sim_users 설정
        user = get_object_or_404(User, uname=user_id)
        user.sim_users.set(User.objects.filter(uname__in=k_users))
        user.save()
        # print('(find_similar_user_pd:74) user.sim_users:', user.sim_users.all())
    else:
        print('user is empty!')
