from pathlib import Path
import re

import pandas as pd

from config import DISEAS_DICT, DATA_PATH, DISEAS_TITLE_DICT
from dbprocessing import desease_match, db_connect, get_query_string

# df = pd.read_csv('/home/igor/Development/med-parsing/output/data.csv')
# # df.describe()

# diseas_columns = ['d0', 'd1', 'd10', 'd11', 'd12',
# 'd13', 'd14', 'd15', 'd16', 'd17', 'd18', 'd19', 'd2', 'd20', 'd21',
# 'd22', 'd23', 'd24', 'd25', 'd26', 'd27', 'd28', 'd3', 'd4', 'd5', 'd6',
# 'd7', 'd8', 'd9']

# disease_df = desease_match(df[['id']]).set_index('id')

df = pd.read_csv('/home/igor/Development/med-parsing/output/table1_data.csv').set_index('id')
# print(df.describe())
"""
Текст диагнозов без болезней
"""
# non_disease_df = df[(df.T == 0).all()]
# conn = db_connect()
# cur = conn.cursor()

# data = tuple(non_disease_df['id'].tolist())
# sql = 'SELECT diagnos FROM diagnosis WHERE patient in %s;'
# cur.execute(sql, (data,))
# for row in cur.fetchall():
#     print(row[0])

# cur.close()
# conn.close()


diseas_columns = ['d0', 'd1', 'd10', 'd11', 'd12', 
    'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9']

# for i in DISEAS_TITLE_DICT.keys():
#     key = f'd{i}'
#     diseas = ' '.join(DISEAS_TITLE_DICT[i])
#     print(f'{i+1}\t{diseas}:\t{(df[key].values == 1).sum()}')

# failure_diseas = len(df[(df.sum(axis=1) == 0)].index) - 1
# print(f' \tДиагноз не определен\t{failure_diseas}')

# p = Path(DATA_PATH).parent
# p = p / 'output'
# csv_path = p / 'disease_diagnos.csv'
# disease_df.to_csv(csv_path, header=True, index=True)
# for i in DISEAS_DICT.keys():
#     key = f'd{i}'
#     diseas = '_'.join(DISEAS_DICT[i])
#     csv_path = p / f'{i + 1} {diseas}.csv'
#     df_for_save = df[df[key] == 1]['id']
#     df_for_save.rename(columns={'id':diseas})
#     df_for_save.to_csv(csv_path, header=True, index=False)

diagnosis_df = df[diseas_columns]

several_diagnos_df = diagnosis_df[diagnosis_df.sum(1) > 1].astype('int')

for diseas in diseas_columns:
    d = {1:'_'.join(DISEAS_TITLE_DICT[int(diseas[1:])]), 0:''}
    several_diagnos_df[diseas] = df[diseas].map(d)

several_diagnos_df['all_diagnosis'] = several_diagnos_df[diseas_columns].apply(lambda x: re.sub(' +', ' ', ' '.join(x).strip()), axis=1)


p = Path(DATA_PATH).parent
p = p / 'output'
csv_path = p / 'several_diagnosis.csv'
several_diagnos_df['all_diagnosis'].to_csv(csv_path, header=True, sep=' ')


# print(get_query_string(DISEAS_DICT[1]))

# conn = db_connect()
# cur = conn.cursor()
# query_string = "SELECT patient, diagnos FROM diagnosis, to_tsquery('russian', '((бронхит) &! (обструктивный | обрструктивный | обрстуктивный | рецидивирующий | хронический | инородное))') query WHERE query @@ meta_diagnos AND ts_rank_cd(meta_diagnos, query) >= 0.05;"
# cur.execute(query_string)
# for row in cur.fetchall():
#     print(row[0])
#     print(row[1])
#     print('---------')
# cur.close()
# conn.close()
