# %% md
# THU THẬP DỮ LIỆU
# %% md

# %%
import os
import requests
import pandas as pd
import time

# %%
# Bảng ánh xạ cặp giao dịch phổ biến cho mỗi sàn
symbol_mapping = {
    "Binance": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"],
    "Coinbase": ["BTC-USD", "ETH-USD", "LTC-USD", "BCH-USD", "ADA-USD"],
    "KuCoin": ["BTC-USDT", "ETH-USDT", "XRP-USDT", "BNB-USDT", "ADA-USDT"],
    "Kraken": ["XXBTZUSD", "XETHZUSD", "XXRPZUSD", "WBTCUSD", "ADAUSD"]
}


# %%
def fetch_binance_klines(symbol, interval='1h', limit=1000, max_records=5000):
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


# %%
def fetch_coinbase_klines(symbol, interval='1m', limit=1000, max_records=5000):
    url = f"https://api.exchange.coinbase.com/products/{symbol}/candles"
    all_data = []

    while len(all_data) < max_records:
        params = {"granularity": 3600}  # 1 phút = 60 giây
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


# %%
def fetch_kucoin_klines(symbol, interval='1hour', limit=1000, max_records=5000):
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


# %%
def fetch_kraken_klines(symbol, interval='60', limit=1000, max_records=5000):
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


# %%
def fetch_data_from_san(symbol, exchange):
    # Chọn hàm thu thập dữ liệu phù hợp dựa trên exchange
    if exchange == "Binance":
        return fetch_binance_klines(symbol)
    elif exchange == "Coinbase":
        return fetch_coinbase_klines(symbol)
    elif exchange == "KuCoin":
        return fetch_kucoin_klines(symbol)
    elif exchange == "Kraken":
        return fetch_kraken_klines(symbol)
    else:
        print(f"Unknown exchange: {exchange}")
        return pd.DataFrame()


# %%
# Tạo các thư mục lưu trữ dữ liệu nếu chưa tồn tại
base_dir = "../data/new_data/raw"
os.makedirs(base_dir, exist_ok=True)

exchanges = ["binance", "coinbase", "kucoin", "kraken"]
for exchange in exchanges:
    os.makedirs(os.path.join(base_dir, exchange), exist_ok=True)


# Thu thập dữ liệu từ tất cả các sàn
def collect_and_save_data():
    for exchange, pairs in symbol_mapping.items():
        for pair in pairs:
            print(f"Fetching data for {pair} from {exchange}...")
            data = fetch_data_from_san(pair, exchange)
            data.to_csv(f"{base_dir}/{exchange.lower()}/{exchange.lower()}_{pair}.csv", index=False)
            print(f"Data for {pair} from {exchange} saved to {exchange.lower()}_{pair}.csv")


collect_and_save_data()