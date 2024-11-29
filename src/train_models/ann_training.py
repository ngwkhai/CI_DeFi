# Import các thư viện cần thiết
import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# Đường dẫn dữ liệu
split_dir = "../data/old_data/splits"
model_dir = "../models"
os.makedirs(model_dir, exist_ok=True)

# Đọc dữ liệu
X_train = pd.read_csv(f"{split_dir}/X_train.csv")
y_train = pd.read_csv(f"{split_dir}/y_train.csv")
X_test = pd.read_csv(f"{split_dir}/X_test.csv")
y_test = pd.read_csv(f"{split_dir}/y_test.csv")

print(f"Kích thước tập train: {X_train.shape}")
print(f"Kích thước tập test: {X_test.shape}")

# Khởi tạo mô hình ANN
model = Sequential([
    Dense(64, activation='relu', input_dim=X_train.shape[1]),  # Lớp đầu tiên
    Dropout(0.2),  # Dropout để giảm overfitting
    Dense(32, activation='relu'),  # Lớp thứ hai
    Dropout(0.2),
    Dense(16, activation='relu'),  # Lớp thứ ba
    Dense(1, activation='sigmoid')  # Lớp đầu ra
])

# Compile mô hình
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Hiển thị kiến trúc mô hình
model.summary()

# Cài đặt Early Stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Huấn luyện mô hình
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=1
)

# Hiển thị lịch sử huấn luyện
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

# Biểu đồ loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

# Biểu đồ accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()

# Lưu mô hình đã huấn luyện
model.save(f"{model_dir}/ann_model.keras")
print("Mô hình ANN đã được lưu tại: ann_model.keras")
