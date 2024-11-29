# Import các thư viện cần thiết
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Đường dẫn dữ liệu
raw_data_dir = "../data/new_data/raw/"
processed_data_dir = "../data/new_data/processed/"
os.makedirs(processed_data_dir, exist_ok=True)

# Danh sách các sàn giao dịch (giả định có trong thư mục raw)
exchanges = ["binance", "coinbase", "kucoin", "kraken"]

# Hợp nhất dữ liệu từ các file raw
all_data = []

for exchange in exchanges:
    exchange_dir = os.path.join(raw_data_dir, exchange)
    files = [f for f in os.listdir(exchange_dir) if f.endswith(".csv")]

    for file in files:
        file_path = os.path.join(exchange_dir, file)
        df = pd.read_csv(file_path)

        all_data.append(df)

# Gộp tất cả dữ liệu
new_data = pd.concat(all_data, ignore_index=True)
print("Dữ liệu sau khi hợp nhất:")
print(new_data.head())

# Loại bỏ giá trị trùng lặp
new_data.drop_duplicates(subset=["time", "pair", "exchange"], inplace=True)

# Kiểm tra giá trị thiếu
missing_values = new_data.isnull().sum()
print("Giá trị thiếu:\n", missing_values)

# Điền giá trị thiếu bằng Interpolation
new_data.interpolate(method="linear", inplace=True)

# Xác nhận không còn giá trị thiếu
print("Giá trị thiếu sau khi xử lý:\n", new_data.isnull().sum())

# Tính các đặc trưng mới
new_data["Price_Change_Pct"] = (new_data["close"] - new_data["open"]) / new_data["open"] * 100
new_data["Volume_Spike"] = new_data["volume"] / new_data["volume"].rolling(window=10).mean()
new_data["Volatility"] = new_data["high"] - new_data["low"]

# Điền NaN trong các cột mới (do rolling)
new_data.fillna(0, inplace=True)

print("Dữ liệu với đặc trưng mới:")
print(new_data[["Price_Change_Pct", "Volume_Spike", "Volatility"]].head())

# Chuẩn hóa các cột đặc trưng
scaler = StandardScaler()
scaled_features = scaler.fit_transform(new_data[["open", "high", "low", "close", "volume", "Price_Change_Pct", "Volume_Spike", "Volatility"]])

# Tạo DataFrame mới cho dữ liệu chuẩn hóa
new_data_scaled = pd.DataFrame(scaled_features, columns=["Open", "High", "Low", "Close", "Volume", "Price_Change_Pct", "Volume_Spike", "Volatility"])

# Thêm lại các cột quan trọng
new_data_scaled["Timestamp"] = new_data["time"].values
new_data_scaled["Pair"] = new_data["pair"].values
new_data_scaled["Exchange"] = new_data["exchange"].values

# Kiểm tra kết quả
print("Dữ liệu đã chuẩn hóa:")
print(new_data_scaled.head())

# Sắp xếp lại các cột theo thứ tự mong muốn
new_data_scaled = new_data_scaled[[
    "Timestamp", "Open", "High", "Low", "Close", "Volume",
    "Pair", "Exchange", "Price_Change_Pct", "Volume_Spike", "Volatility"
]]

# Sắp xếp dữ liệu theo cột Timestamp
new_data_scaled = new_data_scaled.sort_values(by="Timestamp", ascending=True)

# Lưu dữ liệu đã xử lý
processed_file_path = os.path.join(processed_data_dir, "new_data_processed.csv")
new_data_scaled.to_csv(processed_file_path, index=False)
print(f"Dữ liệu đã được sắp xếp và lưu tại: {processed_file_path}")