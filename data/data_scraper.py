import yfinance as yf
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

def get_yahoo_crumb_and_cookies():
    """
    Fetches cookies and crumb from Yahoo Finance for API authentication.
    """
    session = requests.Session()
    url = "https://finance.yahoo.com/quote/AAPL"  # Any valid symbol page to get cookies
    response = session.get(url)
    cookies = session.cookies.get_dict()
    
    crumb_url = "https://query2.finance.yahoo.com/v1/test/getcrumb"
    crumb_response = session.get(crumb_url)
    crumb = crumb_response.text.strip()
    
    return crumb, cookies, session

class YFData:
    def __init__(self):
        pass

    def get_yahoo_tickers(self, exchange='NASDAQ', max_results=10000, region="us"):
        crumb, cookies, session = get_yahoo_crumb_and_cookies()
        
        tickers = []
        offset = 0
        count = 250  # Max per page
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        while offset < max_results:
            url = f"https://query2.finance.yahoo.com/v1/finance/screener?crumb={crumb}&lang=en-US&region={region}&formatted=true&corsDomain=finance.yahoo.com"
            payload = {
                "size": count,
                "offset": offset,
                "sortField": "symbol",
                "sortType": "ASC",
                "quoteType": "EQUITY",
                "topOperator": "AND",
                "query": {
                    "operator": "AND",
                    "operands": [
                        {"operator": "eq", "operands": ["region", region.lower()]},
                        {"operator": "eq", "operands": ["exchange", exchange.upper()]}
                    ]
                }
            }
            
            response = session.post(url, headers=headers, json=payload, cookies=cookies)
            
            if response.status_code != 200:
                print(f"Error: Status code {response.status_code} for exchange {exchange}")
                break
            
            try:
                data = response.json()
                quotes = data.get('finance', {}).get('result', [{}])[0].get('quotes', [])
            except (json.JSONDecodeError, KeyError):
                print("Error parsing response JSON.")
                break
            
            if not quotes:
                break
            
            tickers.extend([q['symbol'] for q in quotes if 'symbol' in q])
            offset += count
            time.sleep(1)  # Delay to avoid rate limiting
            
            if len(quotes) < count:
                break
        
        return tickers
    
    def get_hsi_components(self):
        # Get the HSI ticker data
        hsi = yf.Ticker('^HSI')
        
        # Fetch the components of the index
        components = hsi.constituents
        return components
