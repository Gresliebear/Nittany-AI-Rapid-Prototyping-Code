from alpha_vantage.timeseries import TimeSeries 
import requests
import json 
from pandas import json_normalize
import pandas as pd

statement='Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_MONTHLY_ADJUSTED.'
def time_series_fun_monthly(key, ticker): 
    """ 
    key - API key from aplhavantage
    list_of_tickers = [] list only 
    
    return dataframe
    """

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)
    print(url)
    # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&outputsize=full&apikey=demo&datatype=csv'
    response = requests.get(url)
    
    
    if response.status_code == 200:
        print ('respnse worked!')
    else:
        print ('respnse failed!')
    
    response_dict = response.json()
    # print(response_dict)
    try: 
        if response_dict['Error Message'] == statement:
            return "Ticker is invalid said Alpha"
    except:
        "pass"
    ## validation code
    try:
        _, header= response.json()
    except:
        print("failed")
        return "failed"
    #Convert to pandas dataframe
    df = pd.DataFrame.from_dict(response_dict[header], orient='index')
    #Clean up column names
    df_cols = [i.split(' ')[1] for i in df.columns]
    df.columns = df_cols
    df = df.reset_index(0)
    df.rename(columns = {'index':'Date'}, inplace = True)
        
    return df
