import pandas as pd
from google.cloud import bigquery

client = bigquery.Client()
table_id = "carbon-inkwell-290604.route_in.sentimental_score"

def get_place(sim_users, target_user):
    if len(sim_users) == 1:  # 유사한 유저 1명인 경우
        for i in sim_users:
            sim_users_where = "(" + i + ")"

    else:  # 유사한 유저 여러명
        sim_users_where_temp2 = ""
        for i in sim_users:
            sim_users_where_temp1 = "\'{}\'".format(i) + ","
            sim_users_where_temp2 = sim_users_where_temp2 + sim_users_where_temp1
        sim_users_where = "(" + sim_users_where_temp2 + ")"
        sim_users_where = sim_users_where.replace(",)", ")")

    query_str = """
        SELECT userId, mapId FROM `{}` 
        WHERE 
            userId IN {}
            AND userId != '{}'
            AND score >= '0.5'
    """.format(table_id, sim_users_where, target_user)

    query_job = client.query(
        query_str,
        location="asia-northeast3",
        job_id_prefix="bq_job_get_place_",
    )

    # # 결과값 데이터프레임으로
    # query_df = query_job.to_dataframe()
    # print(query_df)

    sim_place_list = []

    query_result = query_job.result()
    for r in query_result:
        sim_place_list.append([r['userId'], r['mapId']])
    print(sim_place_list)
    return sim_place_list
