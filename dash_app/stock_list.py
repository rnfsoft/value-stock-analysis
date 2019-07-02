import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

def get_sp500():
    res = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    bs = BeautifulSoup(res.text, 'lxml')
    table = bs.find('table', {'class': 'wikitable sortable'})
    stocks = []
    for row in table.findAll('tr')[1:]:
        symbol = row.findAll('td')[0].text.lower().replace('\n', '')
        security = row.findAll('td')[1].text
        stocks.append({'value': symbol, 'label':security})
    return stocks

def get_nasdaq():
    df = pd.read_csv('data/companylist.csv')
    return df.apply(lambda x: {'value': x.Symbol, 'label': x.Name}, axis=1).tolist()

def get_my_stocks():
    stocks = []
    stocks.append({'value':'grpn', 'label': 'Groupon'})
    stocks.append({'value':'tsla', 'label': 'Tesla'})
    stocks.append({'value':'amzn', 'label': 'Amazon'})
    stocks.append({'value':'crwd', 'label': 'Cloud'})
    stocks.append({'value':'lyft', 'label': 'Lyft'})
    stocks.append({'value':'uber', 'label': 'Uber'})
    stocks.append({'value':'work', 'label': 'Slack'})
    return stocks

def combine_stock_list():
    stock_list = get_sp500() + get_my_stocks()
    df = pd.DataFrame(stock_list, columns=['value', 'label'])
    df['value'] = df['value'].str.upper()
    df.drop_duplicates(subset='value', keep='first', inplace=True)
    df.sort_values(by=['value'], inplace=True)
    df['stock_list'] = df.apply(lambda x: {'value': x.value, 'label': '{} ({})'.format(x.label,x.value)}, axis=1)
    return df['stock_list'].tolist()
