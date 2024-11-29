import os

from src.data_collection.binance import fetch_binance_klines
from src.data_collection.coinbase import fetch_coinbase_klines
from src.data_collection.kraken import fetch_kraken_klines
from src.data_collection.kucoin import fetch_kucoin_klines

# Bảng ánh xạ các cặp giao dịch cho từng sàn
symbol_mapping = {
    "binance": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"],
    "coinbase": ["BTC-USD", "ETH-USD", "LTC-USD", "BCH-USD", "ADA-USD"],
    "kucoin": ["BTC-USDT", "ETH-USDT", "XRP-USDT", "BNB-USDT", "ADA-USDT"],
    "kraken": ["XXBTZUSD", "XETHZUSD", "XXRPZUSD", "WBTCUSD", "ADAUSD"]
}

# Hàm ánh xạ sàn với hàm thu thập
fetch_functions = {
    "binance": fetch_binance_klines,
    "coinbase": fetch_coinbase_klines,
    "kucoin": fetch_kucoin_klines,
    "kraken": fetch_kraken_klines
}

# Thu thập dữ liệu từ tất cả các sàn
for exchange, pairs in symbol_mapping.items():
    for pair in pairs:
        print(f"Fetching {exchange} data for {pair}...")

        # Gọi hàm thu thập dữ liệu phù hợp
        fetch_function = fetch_functions[exchange]
        df = fetch_function(symbol=pair)

        # Thư mục lưu dữ liệu
        save_dir = f"../../data/new_data/raw/{exchange.lower()}"

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(save_dir, exist_ok=True)

        # Lưu dữ liệu vào thư mục tương ứng
        save_path = os.path.join(save_dir, f"{exchange}_{pair}.csv")
        df.to_csv(save_path, index=False)
        print(f"Saved {exchange} data for {pair} to {exchange}_{pair}.csv")
