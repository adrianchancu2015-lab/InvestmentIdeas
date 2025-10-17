import yfinance as yf
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

class WikiData:
    def get_index_constituents(self):
        try:
            # Note: This method relies on external sources and can occasionally break.
            # We fetch the S&P 500 components from a known source (e.g., the Fama/French source or similar)
            # A more reliable method is often scraping Wikipedia for the S&P 500 list.
            
            # Example of fetching S&P 500 components via scraping (using pandas' built-in HTML reader)
            sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            
            # Read the HTML tables from the Wikipedia page
            # Set headers to mimic a browser
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

            # Read the HTML tables from the Wikipedia page
            response = requests.get(sp500_url, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Get the HTML content
                html_content = response.text

            tables = pd.read_html(html_content)

            sp500_df = tables[0] # The first table usually contains the list
            
            sp500_tickers = sp500_df['Symbol'].tolist()
            
            print(f"\nRetrieved {len(sp500_tickers)} S&P 500 tickers via Wikipedia scraping.")
            print("Sample S&P 500 Tickers:", sp500_tickers[:5])
            return sp500_tickers
        except ImportError:
            print("\npandas_datareader is not installed. Skipping index component example.")
        except Exception as e:
            print(f"\nCould not retrieve S&P 500 list: {e}")

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
