import scraper as scp

def get_discount_rate():
    url = 'https://ycharts.com/indicators/us_discount_rate'
    discount_rate = float(scp.scrape_tables(url).iloc[0,2].strip('%'))/100
    return discount_rate

FISCAL_YEARS = 5

DISCOUNT_RATE = 0.03

TARGET_YEARS = 5

MARGIN_RATE = 0.2
