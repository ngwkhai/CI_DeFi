import os
import requests
import pandas as pd
import time

base_dir = "../data/new_data/raw"

# Lấy danh sách cặp giao dịch từ Binance
def get_binance_pairs():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    pairs = [symbol["symbol"] for symbol in data["symbols"] if symbol["status"] == "TRADING"]
    return pairs[:20]

# Lấy danh sách cặp giao dịch từ Coinbase
def get_coinbase_pairs():
    url = "https://api.exchange.coinbase.com/products"
    response = requests.get(url)
    data = response.json()
    pairs = [product["id"] for product in data]
    return pairs[:20]

# Lấy danh sách cặp giao dịch từ KuCoin
def get_kucoin_pairs():
    url = "https://api.kucoin.com/api/v1/symbols"
    response = requests.get(url)
    data = response.json()
    pairs = [symbol["symbol"] for symbol in data["data"] if symbol["enableTrading"]]
    return pairs[:20]

# Lấy danh sách cặp giao dịch từ Kraken
def get_kraken_pairs():
    url = "https://api.kraken.com/0/public/AssetPairs"
    response = requests.get(url)
    data = response.json()
    pairs = list(data["result"].keys())
    return pairs[:20]

binance_pairs = get_binance_pairs()
coinbase_pairs = get_coinbase_pairs()
kucoin_pairs = get_kucoin_pairs()
kraken_pairs = get_kraken_pairs()

# Kiểm tra danh sách
print(f"Binance pairs: {binance_pairs}")
print(f"Coinbase pairs: {coinbase_pairs}")
print(f"KuCoin pairs: {kucoin_pairs}")
print(f"Kraken pairs: {kraken_pairs}")


def fetch_binance_klines(symbol, interval='1h', limit=1000):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data or isinstance(data, dict):
        print(f"No data or error for {symbol} from Binance: {data}")
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
        "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df["pair"] = symbol[:-3] + "-" + symbol[-3:]
    df["exchange"] = "Binance"
    return df[["time", "open", "high", "low", "close", "volume", "pair", "exchange"]][:100]

def fetch_binance_klines(symbol, interval='1h', limit=1000):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data or isinstance(data, dict):  # Trường hợp lỗi hoặc không có dữ liệu
        print(f"No data or error for {symbol} from Binance: {data}")
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
        "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df["pair"] = symbol[:-3] + "-" + symbol[-3:]
    df["exchange"] = "Binance"
    return df[["time", "open", "high", "low", "close", "volume", "pair", "exchange"]][:100]

def fetch_coinbase_klines(symbol, interval='1h', limit=1000):
    url = f"https://api.exchange.coinbase.com/products/{symbol}/candles"
    params = {"granularity": 3600}  # 1h

    response = requests.get(url, params=params)
    data = response.json()

    if not data or isinstance(data, dict):  # Trường hợp lỗi hoặc không có dữ liệu
        print(f"No data or error for {symbol} from Coinbase: {data}")
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["pair"] = symbol  # Pair đã định dạng sẵn từ Coinbase (ví dụ: BTC-USD)
    df["exchange"] = "Coinbase"
    return df[["time", "open", "high", "low", "close", "volume", "pair", "exchange"]][:100]


def fetch_kucoin_klines(symbol, interval='1hour', limit=1000):
    url = "https://api.kucoin.com/api/v1/market/candles"
    params = {"symbol": symbol, "type": interval}

    response = requests.get(url, params=params)
    data = response.json()

    if "data" not in data or not data["data"]:
        print(f"No data or error for {symbol} from KuCoin: {data}")
        return pd.DataFrame()

    df = pd.DataFrame(data["data"], columns=["time", "open", "close", "high", "low", "volume", "close_time"])
    # Chuyển đổi cột `time` thành Unix timestamp (nếu chưa phải kiểu số)
    if df["time"].dtype == "object":  # Nếu `time` là chuỗi
        df["time"] = df["time"].astype(float).astype(int)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["pair"] = symbol
    df["exchange"] = "KuCoin"
    return df[["time", "open", "high", "low", "close", "volume", "pair", "exchange"]][:100]

def fetch_kraken_klines(symbol, interval='60', limit=1000):
    url = "https://api.kraken.com/0/public/OHLC"
    params = {"pair": symbol, "interval": interval}

    response = requests.get(url, params=params)
    data = response.json()

    if "result" not in data or symbol not in data["result"]:
        print(f"No data or error for {symbol} from Kraken: {data}")
        return pd.DataFrame()

    df = pd.DataFrame(data["result"][symbol], columns=[
        "time", "open", "high", "low", "close", "volume", "ignore1", "ignore2"
    ])
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["pair"] = symbol[:-3] + "-" + symbol[-3:]
    df["exchange"] = "Kraken"
    return df[["time", "open", "high", "low", "close", "volume", "pair", "exchange"]][:100]


# Hàm thu thập dữ liệu từ các cặp giao dịch chính
def fetch_data_for_top_pairs(exchange, pairs, fetch_func, limit=1000):
    all_data = []

    for pair in pairs:
        print(f"Fetching data for {pair} from {exchange}...")
        try:
            data = fetch_func(pair, limit=limit)
            if not data.empty:
                all_data.append(data)
                print(f"Collected {len(data)} rows for {pair}.")
        except Exception as e:
            print(f"Error fetching data for {pair} from {exchange}: {e}")

    # Gộp tất cả dữ liệu
    all_data = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    return all_data


# Hàm gọi lời thu thập và lưu trữ giữ liệu
def fetch_top_pairs_data():
    for exchange, pairs, fetch_func in [
        ("Binance", binance_pairs, fetch_binance_klines),
        ("Coinbase", coinbase_pairs, fetch_coinbase_klines),
        ("KuCoin", kucoin_pairs, fetch_kucoin_klines),
        ("Kraken", kraken_pairs, fetch_kraken_klines),
    ]:
        print(f"Collecting data for {exchange}...")
        data = fetch_data_for_top_pairs(exchange, pairs, fetch_func, limit=1000)

        # Lưu dữ liệu nếu có
        if not data.empty:
            file_path = f"{base_dir}/{exchange.lower()}/{exchange.lower()}.csv"
            data.to_csv(file_path, index=False)
            print(f"Saved data for {exchange} to {file_path}.")
        else:
            print(f"No data collected for {exchange}.")

fetch_top_pairs_data()