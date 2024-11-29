# Import các thư viện cần thiết
import os
import pandas as pd
from tensorflow.keras.models import load_model
import joblib
import matplotlib.pyplot as plt

# Đường dẫn dữ liệu và mô hình
processed_data_path = "../data/new_data/processed/new_data_processed.csv"
ann_model_path = "../models/ann_model.keras"
svm_model_path = "../models/svm_model.pkl"
output_file_path = "../data/new_data/predict"
os.makedirs(output_file_path, exist_ok=True)

# Tải dữ liệu đã xử lý
new_data = pd.read_csv(processed_data_path)
print("Dữ liệu đã xử lý:")
print(new_data.head())

# Đảm bảo cột `Timestamp` là datetime
new_data["Timestamp"] = pd.to_datetime(new_data["Timestamp"])

# Tải mô hình ANN đã huấn luyện
ann_model = load_model(ann_model_path)

# Chọn các cột đặc trưng
features = ["Open", "High", "Low", "Close", "Volume", "Price_Change_Pct", "Volume_Spike", "Volatility"]

# Trích xuất đặc trưng từ ANN
new_data_features = ann_model.predict(new_data[features])
print(f"Kích thước đặc trưng từ ANN: {new_data_features.shape}")

# Tải mô hình SVM đã huấn luyện
svm_model = joblib.load(svm_model_path)

# Dự đoán nhãn cho dữ liệu mới
# Ngưỡng dự đoán
threshold = 0.5
new_data["Predicted_Label"] = (svm_model.predict_proba(new_data_features)[:, 1] > threshold).astype(int)


# Hiển thị phân phối nhãn
print("Phân phối nhãn dự đoán:")
print(new_data["Predicted_Label"].value_counts())

# Lưu kết quả dự đoán
new_data_sorted = new_data.sort_values(by="Timestamp")
new_data_sorted.to_csv(f"{output_file_path}/new_data_predictions.csv", index=False)
print(f"Kết quả đã được lưu tại: {output_file_path}")

# Vẽ biểu đồ phân phối nhãn
new_data["Predicted_Label"].value_counts().plot(kind="bar", color="skyblue")
plt.title("Phân phối nhãn dự đoán trên dữ liệu mới")
plt.xlabel("Label")
plt.ylabel("Số lượng")
plt.show()
