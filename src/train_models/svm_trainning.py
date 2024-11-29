# Import các thư viện
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import load_model

from sklearn.svm import SVC
import joblib

# Đường dẫn dữ liệu và mô hình
split_dir = "../data/old_data/splits"
model_dir = "../models"
svm_model_path = f"{model_dir}/svm_model.pkl"

# Đọc dữ liệu
X_train = pd.read_csv(f"{split_dir}/X_train.csv")
y_train = pd.read_csv(f"{split_dir}/y_train.csv")
X_test = pd.read_csv(f"{split_dir}/X_test.csv")
y_test = pd.read_csv(f"{split_dir}/y_test.csv")

# Kiểm tra dữ liệu
print(f"Kích thước tập train: {X_train.shape}")
print(f"Kích thước tập test: {X_test.shape}")

# Tải mô hình ANN đã huấn luyện
ann_model = load_model(f"{model_dir}/ann_model.keras")

# Trích xuất đặc trưng từ ANN
X_train_features = ann_model.predict(X_train)
X_test_features = ann_model.predict(X_test)

# Kiểm tra kích thước đặc trưng
print(f"Kích thước đặc trưng tập train: {X_train_features.shape}")
print(f"Kích thước đặc trưng tập test: {X_test_features.shape}")

# Khởi tạo và huấn luyện SVM
svm_model = SVC(kernel='rbf', probability=True, class_weight='balanced', random_state=42)
svm_model.fit(X_train_features, y_train.values.ravel())

# Lưu mô hình SVM
joblib.dump(svm_model, svm_model_path)
print(f"Mô hình SVM đã được lưu tại: {svm_model_path}")

# Dự đoán trên tập validation
y_test_pred = svm_model.predict(X_test_features)

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix:\n", conf_matrix)

# Báo cáo chi tiết
print("Classification Report:\n", classification_report(y_test, y_test_pred))
