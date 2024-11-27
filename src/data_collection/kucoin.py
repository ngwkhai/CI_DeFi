import requests
import pandas as pd
import time

def fetch_kucoin_klines(symbol, interval='1min', limit=1000, max_records=5000):
    url = "https://api.kucoin.com/api/v1/market/candles"
    all_data = []

    while len(all_data) < max_records:
        params = {
            "symbol": symbol,
            "type": interval  # 1min cho mỗi nến 1 phút
        }
        response = requests.get(url, params=params)
        data = response.json()["data"]

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

    df = pd.DataFrame(all_data[:max_records], columns=["time", "open", "close", "high", "low", "volume", "close_time"])
    # Chuyển đổi cột `time` thành Unix timestamp (nếu chưa phải kiểu số)
    if df["time"].dtype == "object":  # Nếu `time` là chuỗi
        df["time"] = df["time"].astype(float).astype(int)

    # Chuyển đổi `time` thành định dạng datetime
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["exchange"] = "KuCoin"
    df["pair"] = symbol
    return df[["time", "open", "high", "low", "close", "volume", "exchange", "pair"]]
