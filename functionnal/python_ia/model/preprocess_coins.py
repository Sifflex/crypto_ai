import pandas as pd

import datetime


def normalize(df):
    result = df.copy()
    for feature_name in ['open', 'high', 'low', 'close', 'Volume BTC', 'Volume USDT']:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result

def as_day(date_str):
    date, hour = date_str.split(' ')
    y,m,d = date.split('-')
    return int(datetime.datetime(int(y), int(m), int(d)).weekday())
def as_hour(date_str):
    date, hour = date_str.split(' ')
    h,_,_ = hour.split(':')
    return int(h)

def execute(path):
    df = pd.read_csv(path, 
            usecols = 
            ['unix', 
            'date', 
            'symbol', 
            'open', 
            'high', 
            'low', 
            'close', 
            'Volume BTC', 'Volume USDT', 'tradecount'])
    #df = normalize(df) #normalizing data
    df['day_of_the_week'] = df['date'].apply(as_day)
    df['hour_of_the_day'] = df['date'].apply(as_hour)
    df_clean = df.copy()
    df_clean.drop(columns=['tradecount', 'symbol', 'unix', 'date'], inplace=True) #Droping unusable columns
    return df_clean

    
