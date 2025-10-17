from data.data_scraper import YFData, WikiData

if __name__=="__main__":
    dataloader = WikiData()
    result = dataloader.get_index_constituents()
    print(result)