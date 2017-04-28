import json
import pandas as pd
from glob import glob

def read():
    df = pd.read_csv('data/processed/slack_messages.csv')
    sub = df[['channel', 'name']]
    comment_counts = sub.groupby(['name', 'channel']).size().unstack('channel')
    comment_counts.fillna(0, inplace=True)
    return comment_counts

def transform():
    d = []
    for f_name in glob('data/raw/*/*.json'):
        with open(f_name) as f:
            data = json.load(f,encoding='utf-8')
            for i in data:
                i['channel'] = f_name.split('/')[-2]
                d.append(i)

    df = pd.DataFrame(d)
    cols_to_drop = df.columns.difference(['channel', 'text', 'ts', 'user'])
    df.drop(cols_to_drop, axis=1, inplace=True)

    #users
    users = pd.read_json('data/raw/users.json')
    users = users[users.deleted == False]
    users = users[users.is_bot == False]
    cols_to_drop = users.columns.difference(['id', 'name', 'real_name', 'tz'])
    users.drop(cols_to_drop, axis=1, inplace=True)

    df = pd.merge(df, users, left_on='user', right_on='id')
    df.to_csv('data/processed/slack_messages.csv', index=False, encoding='utf-8')
