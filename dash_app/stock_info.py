from datetime import datetime, timedelta

import pandas as pd
import settings
from converter import number_converter
from pandas_datareader import data as web
from scraper import scrape_tables


def get_stock_info(symbol):
    global df_price_history
    global df_income_statement, df_raw_income_statement
    global df_balance_sheet, df_raw_balance_sheet
    global df_year_end_adj_close

    df_price_history = get_price_history(symbol)
    df_raw_income_statement, df_income_statement = get_income_statement(symbol)
    df_raw_balance_sheet, df_balance_sheet = get_balance_sheet(symbol)
    df_year_end_adj_close = get_year_end_adj_close()

def get_price_history(symbol, start_date=datetime.now()-timedelta(settings.FISCAL_YEARS*365), end_date=datetime.now()):
    return web.DataReader(symbol, data_source='yahoo', start=start_date, end=end_date)

def parse_reports(url, rows):
    df = scrape_tables(url).fillna('') # to concatenate df.columns[0] and df.columns[7]
    df['-'] = df[df.columns[0]].str.cat(df[df.columns[7]])
    df.set_index('-', inplace=True)
    df.drop(df.columns[[0,6,7]], 1, inplace=True)
    df_raw = df.loc[rows,:]
    df = df_raw.applymap(lambda x:number_converter(x)).replace('-', '0').astype('float64') # converted to number
    return df_raw, df

def get_income_statement(symbol):
    url = 'https://www.marketwatch.com/investing/stock/'+symbol+'/financials'
    rows = ['EPS (Basic)','EPS (Basic) Growth','Net Income', 'Interest Expense', 'EBITDA', ]
    return parse_reports(url,rows)

def get_balance_sheet(symbol):
    url = 'https://www.marketwatch.com/investing/stock/'+symbol+'/financials/balance-sheet'
    rows = ['Total Current Assets','Long-Term Debt','Total Shareholders\' Equity']
    return parse_reports(url,rows)

def get_year_end_adj_close():
    df_price_history['Year'] = pd.DatetimeIndex(df_price_history.index).year
    
    df = pd.DataFrame(df_price_history.groupby('Year').tail(1).set_index('Year')[:settings.FISCAL_YEARS]['Adj Close'])
    df.index = df.index.map(str)
    df = df.T.round(2)
    return df

def combine_financial_reports():
    df = pd.concat([df_raw_income_statement, df_raw_balance_sheet])
    df.index.name = '-'
    return df



# get_stock_info('AMZN')
# print(get_year_end_adj_close())
