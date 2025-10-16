from data.data_scraper import YFData

if __name__=="__main__":
    dataloader = YFData()
    result = dataloader.get_yahoo_tickers(exchange="NMS")
    print(result)