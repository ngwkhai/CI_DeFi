import requests
import pandas as pd
import time

def fetch_coinbase_klines(symbol, interval='1m', limit=1000, max_records=5000):
    url = f"https://api.exchange.coinbase.com/products/{symbol}/candles"
    all_data = []

    while len(all_data) < max_records:
        params = {"granularity": 60}  # 1 phút = 60 giây
        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            print(f"No data returned for {symbol}.")
            break

        if isinstance(data, list) and len(data) > 0:
            all_data.extend(data)
        else:
            print(f"Unexpected data structure for {symbol}: {data}")
            break

        time.sleep(0.5)  # Tránh vượt quá giới hạn API

    if not all_data:
        print(f"No data collected for {symbol}.")
        return pd.DataFrame()

    df = pd.DataFrame(all_data[:max_records], columns=["time", "low", "high", "open", "close", "volume"])
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["exchange"] = "Coinbase"
    df["pair"] = symbol
    return df[["time", "open", "high", "low", "close", "volume", "exchange", "pair"]]
