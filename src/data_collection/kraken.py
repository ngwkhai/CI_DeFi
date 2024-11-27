import requests
import pandas as pd
import time


def fetch_kraken_klines(symbol, interval='1', limit=1000, max_records=5000):
    url = "https://api.kraken.com/0/public/OHLC"
    all_data = []

    while len(all_data) < max_records:
        params = {
            "pair": symbol,
            "interval": interval  # 1 phút = 1
        }
        response = requests.get(url, params=params)
        data = response.json()
        # Kiểm tra nếu 'result' có trong dữ liệu trả về
        if "result" in data and symbol in data["result"]:
            data = data["result"][symbol]  # Lấy dữ liệu từ trường 'result'
        else:
            print(f"Unexpected data structure or empty result for {symbol}: {data}")
            break
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
    df = pd.DataFrame(all_data[:max_records],
                      columns=["time", "open", "high", "low", "close", "volume", "close_time", "ignore"])
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["exchange"] = "Kraken"
    df["pair"] = symbol
    return df[["time", "open", "high", "low", "close", "volume", "exchange", "pair"]]