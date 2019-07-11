import numpy as np
import pandas as pd
import settings
import stock_info
from scraper import scrape_tables


def CAGR(start_value, end_value, years=settings.FISCAL_YEARS):   
    return ((end_value - start_value + np.abs(start_value))/np.abs(start_value))**(1/years)-1

def get_annual_growth(symbol):
    url = 'https://www.nasdaq.com/symbol/' + symbol + '/earnings-growth'
    df = scrape_tables(url).fillna('')
    df.to_csv('test.csv')

def get_future_value():
    df_income_statement = stock_info.df_income_statement
    data = []
    df_future_value = pd.DataFrame(None, index= [0], columns=['Annual Growth Rate', 'Last EPS', 'Future EPS (+5 Years)', 'MEAN PE', 
                                            'FV (Future EPS x PE)','PV (Future EPS x PE)', 'Margin Price (PV x 80%)',
                                            'Last Share Price','Recommendation' ])
    
    eps = df_income_statement.loc['EPS (Basic)',]
    annual_growth_rate = CAGR(eps[0], eps[-1])

    if np.isnan(annual_growth_rate):
        pass
    else:
        df_future_value['Annual Growth Rate'] = 0.3 if annual_growth_rate > 3.0 else annual_growth_rate # max 30% growth
        df_future_value['Last EPS'] = eps[-1]
        df_future_value['Future EPS (+5 Years)'] = abs(np.fv(df_future_value['Annual Growth Rate'],settings.TARGET_YEARS, 0, df_future_value['Last EPS']))
        df_future_value['MEAN PE'] = get_mean_pe_ratio(eps.values)
        df_future_value['FV (Future EPS x PE)'] = df_future_value['Future EPS (+5 Years)'] * df_future_value['MEAN PE']
        df_future_value['PV (Future EPS x PE)'] = abs(np.pv(settings.DISCOUNT_RATE, settings.TARGET_YEARS,0,df_future_value['FV (Future EPS x PE)']))
        df_future_value['Margin Price (PV x 80%)'] =  df_future_value['PV (Future EPS x PE)'] * (1 - settings.MARGIN_RATE)
        df_future_value['Last Share Price'] = stock_info.df_price_history['Adj Close'].tail(1).values[0]
        df_future_value = df_future_value.round(2)
        df_future_value['BUY/SELL'] = np.where((df_future_value['Last Share Price'] < df_future_value['Margin Price (PV x 80%)']), 'BUY', 'SELL')
    df_future_value.set_index(['Annual Growth Rate'], inplace=True)
    return df_future_value

def get_mean_pe_ratio(eps):
    df_price_history = stock_info.df_price_history
    df_price_history['Year'] = pd.DatetimeIndex(df_price_history.index).year
    df_min_pe_ratio = df_price_history.groupby('Year').tail(1).set_index('Year')[:settings.FISCAL_YEARS]

    df_min_pe_ratio['PE'] = df_min_pe_ratio['Adj Close'] / eps
    return None if df_min_pe_ratio['PE'].mean() < 0 else df_min_pe_ratio['PE'].mean()




