import requests
import pandas as pd
import time

def fetch_binance_klines(symbol, interval='1m', limit=1000, max_records=5000):
    url = "https://api.binance.com/api/v1/klines"
    all_data = []

    while len(all_data) < max_records:
        params = {
            "symbol": symbol,
            "interval": interval,  # Khoảng thời gian của mỗi nến (ví dụ: 1m, 5m, 1h, 1d, ...)
            "limit": limit  # Tối đa 1000 nến mỗi lần
        }

        response = requests.get(url, params=params)
        data = response.json()

        # Kiểm tra dữ liệu trả về
        if not data:
            print(f"No data returned for {symbol}.")
            break

        # Kiểm tra cấu trúc dữ liệu trả về
        if isinstance(data, list) and len(data) > 0:
            all_data.extend(data)
        else:
            print(f"Unexpected data structure for {symbol}: {data}")
            break

        time.sleep(0.5)  # Tránh vượt quá giới hạn API

    if not all_data:
        print(f"No data collected for {symbol}.")
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu không có dữ liệu

    # Chuyển đổi dữ liệu thành DataFrame và trả về
    df = pd.DataFrame(all_data[:max_records],
                      columns=["time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
                               "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df["exchange"] = "Binance"
    df["pair"] = symbol  # Thêm thông tin cặp giao dịch
    return df[["time", "open", "high", "low", "close", "volume", "exchange", "pair"]]
