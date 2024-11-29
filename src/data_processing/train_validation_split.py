# Import các thư viện cần thiết
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

# Đường dẫn dữ liệu
data_path = "../data/old_data/processed/data_processed.csv"
split_dir = "../data/old_data/splits"
os.makedirs(split_dir, exist_ok=True)

# Đọc dữ liệu đã xử lý
data = pd.read_csv(data_path)
print("Dữ liệu ban đầu:")
print(data.head())

# Xác định các cột đặc trưng và nhãn
features = ["Open", "High", "Low", "Close", "Volume", "Price_Change_Pct", "Volume_Spike", "Volatility"]
X = data[features]
y = data["Label"]

print("Số lượng mẫu dữ liệu:", X.shape[0])
print("Phân phối nhãn:\n", y.value_counts())

# Chia dữ liệu thành train (80%) và test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Kích thước tập huấn luyện: {X_train.shape[0]}")
print(f"Kích thước tập kiểm tra: {X_test.shape[0]}")

# Khởi tạo SMOTE
smote = SMOTE(random_state=42)

# Tạo dữ liệu cân bằng
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# Kiểm tra lại phân phối nhãn sau SMOTE
print("Phân phối nhãn sau SMOTE:")
print(pd.Series(y_train_balanced).value_counts())

# Lưu tập train và test
X_train_balanced.to_csv(f"{split_dir}/X_train.csv", index=False)
y_train_balanced.to_csv(f"{split_dir}/y_train.csv", index=False)

X_test.to_csv(f"{split_dir}/X_test.csv", index=False)
y_test.to_csv(f"{split_dir}/y_test.csv", index=False)

print("Dữ liệu đã được chia và lưu tại:", split_dir)
