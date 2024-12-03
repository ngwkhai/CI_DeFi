import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Đường dẫn thư mục
data_dir = "../data/old_data/"
processed_dir = os.path.join(data_dir, "processed")
plot_dir = "../plots/data_analysis"

# Tạo thư mục lưu trữ dữ liệu nếu chưa có
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# Danh sách các sàn giao dịch
exchanges = ["binance", "bittrex", "kraken", "kucoin", "lbank"]

# Hợp nhất dữ liệu từ các file CSV
all_data = []

for exchange in exchanges:
    exchange_dir = os.path.join(data_dir, "raw", exchange)
    files = [f for f in os.listdir(exchange_dir) if f.endswith(".csv")]

    for file in files:
        file_path = os.path.join(exchange_dir, file)
        df = pd.read_csv(file_path)

        # Lấy thông tin cặp giao dịch từ tên file
        pair = file.split("_")[1]

        # Thêm cột thông tin
        df["Pair"] = pair
        df["Exchange"] = exchange
        all_data.append(df)

# Hợp nhất toàn bộ dữ liệu
data = pd.concat(all_data, ignore_index=True)
print("Dữ liệu ban đầu:")
print(data.head())

# Vẽ biểu đồ phân phối Volume
plt.figure(figsize=(10, 6))
sns.histplot(data["Volume"], bins=50, kde=True, color='blue')
plt.title("Phân Phối Khối Lượng Giao Dịch (Volume)")
plt.xlabel("Volume")
plt.ylabel("Tần suất")
plt.savefig(os.path.join(plot_dir, "volume_distribution.png"))
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(data["Timestamp"], data["High"], label='Giá Cao Nhất (High)', color='green')
plt.plot(data["Timestamp"], data["Low"], label='Giá Thấp Nhất (Low)', color='red')
plt.title("Biến Động Giá Theo Thời Gian")
plt.xlabel("Thời gian")
plt.ylabel("Giá")
plt.legend()
plt.savefig(os.path.join(plot_dir, "price_volatility.png"))
plt.show()

plt.figure(figsize=(8, 6))
correlation = df[["Open", "High", "Low", "Close", "Volume"]].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Ma Trận Tương Quan Giữa Các Đặc Trưng")
plt.savefig(os.path.join(plot_dir, "correlation_matrix.png"))
plt.show()

# Chuyển Timestamp sang datetime
data["Timestamp"] = pd.to_datetime(data["Timestamp"])

# Loại bỏ giá trị trùng lặp
data.drop_duplicates(subset=["Timestamp", "Pair", "Exchange"], inplace=True)

# Sắp xếp dữ liệu
data.sort_values(by="Timestamp", inplace=True)
print(data.info())

# Kiểm tra giá trị thiếu
missing_values = data.isnull().sum()
print("Giá trị thiếu:\n", missing_values)

# Điền giá trị thiếu bằng phương pháp Linear Interpolation
data.interpolate(method="linear", inplace=True)

# Xác nhận lại không còn giá trị thiếu
print("Giá trị thiếu after sau khi điền:\n", data.isnull().sum())

# Tính toán các đặc trưng mới
data["Price_Change_Pct"] = (data["Close"] - data["Open"]) / data["Open"] * 100
data["Volume_Spike"] = data["Volume"] / data["Volume"].rolling(window=10).mean()
data["Volatility"] = data["High"] - data["Low"]

# Điền NaN trong cột mới (do rolling tạo ra)
data.fillna(0, inplace=True)


print("Dữ liệu với đặc trưng mới:")
print(data[["Price_Change_Pct", "Volume_Spike", "Volatility"]].head())

# Chuẩn hóa các cột
scaler = MinMaxScaler()

columns_to_scale = ["Open", "High", "Low", "Close", "Volume"]
data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])

print("Dữ liệu sau chuẩn hóa:")
print(data.head())

# Lưu dữ liệu đã xử lý
processed_file = os.path.join(processed_dir, "data_processed.csv")
data.to_csv(processed_file, index=False)
print(f"Dữ liệu đã lưu tại: {processed_file}")
