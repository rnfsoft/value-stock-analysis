#These functions were developed by Colin OKeefe for realpython.com.
#Link: https://realpython.com/python-web-scraping-practical-introduction/

from contextlib import closing

import pandas as pd
from requests import get
from requests.exceptions import RequestException


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def scrape_tables(url):
    df_list = []
    raw_html = simple_get(url)
    for df in pd.read_html(raw_html):
        df_list.append(df)
    return pd.concat(df_list, sort=False)
