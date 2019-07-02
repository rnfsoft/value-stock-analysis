import time

import pandas as pd
import settings
import stock_info


def get_stock_evaluation():
    df_financial_reports = pd.concat([stock_info.df_income_statement, stock_info.df_balance_sheet])

    eligibility = {
        'growth': 0,
        'roe' : 0.13,
        'roa' : 0.07,
        'ltd': 5,
        'icr' : 3
    }
    evaluation = []

    growth = df_financial_reports.loc['EPS (Basic) Growth', ]
    evaluation.append('Negative growth exists' if any(growth[growth < eligibility['growth']]) else None)
 
    roe = (df_financial_reports.loc['Net Income', ]/df_financial_reports.loc['Total Shareholders\' Equity', ]).mean() < eligibility['roe']
    evaluation.append('ROE mean < ' + str(eligibility['roe']) if roe else None)

    roa = (df_financial_reports.loc['Net Income', ]/df_financial_reports.loc['Total Current Assets', ]).mean() < eligibility['roa']
    evaluation.append('ROA mean < ' + str(eligibility['roa']) if roa else None)

    # Long Term Debt 
    ltd = df_financial_reports.loc['Long-Term Debt', df_financial_reports.columns[-1]] > eligibility['ltd'] * df_financial_reports.loc['Net Income', df_financial_reports.columns[-1]]
    evaluation.append('Long term debt > Net income x ' + str(eligibility['ltd']) if ltd else None)

    # Interest Coverage Ratio = EBIT / Interest expenses
    icr = df_financial_reports.loc['EBITDA', df_financial_reports.columns[-1]] < eligibility['icr'] * df_financial_reports.loc['Interest Expense', df_financial_reports.columns[-1]]
    evaluation.append('Interest Coverage Ratio < ' + str(eligibility['icr']) if icr else None)
    return evaluation
