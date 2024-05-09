import requests
import pandas as pd
from config import *

def gen_ticker_format(symbol: str, indicators: str | list):
    if isinstance(indicators, list):
        str_indicators = ','.join(indicators)
        return f'{symbol}-{str_indicators}'
    else: 
        return f'{symbol}-{indicators}'
    
def gen_option_config(info_df: pd.DataFrame):
    config = set()
    
    info_df = info_df[info_df['交易時段'] == '一般']
    info_df['到期月份(週別)'] = info_df['到期月份(週別)'].str.strip()
    
    if OPTION_TYPE == 'week':
        info_df = info_df[info_df['到期月份(週別)'].apply(lambda x : 'W' in x)]
        week = info_df['到期月份(週別)'].unique()[0].split('W')[-1]
        xq_option_name = f'TX{week}N{MONTH}'
        
    else:
        expire_date = f'{YEAR}{MONTH}'
        
        info_df = info_df[info_df['到期月份(週別)'] == expire_date] 
        xq_option_name = f'TXON{MONTH}'
    
    if info_df.empty:
        raise ValueError(f'Config Error: {OPTION_TYPE} {YEAR}{MONTH}') 
    for index, values in info_df.iterrows():
        s_price = int(float(values.get('履約價')))
        config.add(f'{xq_option_name}C{s_price}.TF')
        config.add(f'{xq_option_name}P{s_price}.TF')
    return config


def get_option_info(input_date = ''):
    from datetime import date
    import csv
    
    if input_date:
        pass
    else:
        today_str = str(date.today()).replace('-', '/')
        
    payload =  {
        'down_type':1 , 
        'commodity_id':'TXO',
        'queryStartDate':today_str,
        'queryEndDate': today_str,
        'commodity_idt':'TXO' 
        }
    res = requests.post(f'https://www.taifex.com.tw/cht/3/optDataDown', data = payload, timeout= 3)
    scsv = res.text
    data = []
    reader = csv.reader(scsv.split('\n'), delimiter=',')
    for row in reader:
        data.append(row)
        df = pd.DataFrame(data)
    df.columns = df.iloc[0].values.tolist()
    df = df.iloc[1:]
    config = gen_option_config(df)
    
    return config
    



# def create_option_tickers():
#     pass

