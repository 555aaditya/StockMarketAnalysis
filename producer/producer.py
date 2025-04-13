from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
import os
import json
from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()
API_KEY = os.getenv('API_KEY')
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
TOPIC_NAME = 'stock-data'

ts = TimeSeries(key=API_KEY, output_format='pandas')

def custom_serializer(obj):
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v, default=custom_serializer).encode('utf-8')
)

def fetch_stock_data():     
    data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='compact')

    data = data.reset_index()
    data.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    print(data.head(1).to_string(index=False))

    latest = data.iloc[0].to_dict()
    print("📤 Sending to Kafka:", latest)
    producer.send(TOPIC_NAME, latest)
    producer.flush() 

if __name__ == "__main__":
    while True:
        fetch_stock_data()
        time.sleep(60)