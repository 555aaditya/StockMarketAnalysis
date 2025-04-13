from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

ts = TimeSeries(key=API_KEY, output_format='pandas')

def fetch_stock_data():     
    data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='compact')

    data = data.reset_index()
    data.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    print(data.head(1).to_string(index=False))

if __name__ == "__main__":
    while True:
        fetch_stock_data()
        time.sleep(60)