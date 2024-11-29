# Dự án Phát Hiện Gian Lận Trong Giao Dịch Tài Chính

Dự án này tập trung vào việc xây dựng và áp dụng các mô hình học máy để phát hiện các giao dịch gian lận trong lĩnh vực giao dịch tiền mã hóa. Quy trình bao gồm các bước: thu thập dữ liệu, tiền xử lý, huấn luyện mô hình, và áp dụng mô hình đã huấn luyện lên tập dữ liệu mới.

---

## Tổng Quan Về Dự Án

Dự án được tổ chức thành các giai đoạn và được triển khai trong từng tệp Jupyter Notebook khác nhau như sau:

1. **Xử lý dữ liệu cũ (Old Data Processing)**: 
   - Làm sạch và tiền xử lý dữ liệu lịch sử.
   - Cân bằng dữ liệu với SMOTE để giải quyết vấn đề mất cân bằng giữa nhãn "gian lận" và "không gian lận".

2. **Chia dữ liệu (Train Validation Split)**: 
   - Chia dữ liệu cũ đã tiền xử lý thành các tập huấn luyện, kiểm tra và xác thực.

3. **Huấn luyện mô hình (Model Training)**:
   - **ANN (Artificial Neural Network)**: Được sử dụng để học và trích xuất các đặc trưng từ dữ liệu.
   - **SVM (Support Vector Machine)**: Sử dụng ANN như bộ trích xuất đặc trưng và thực hiện phân loại giao dịch.

4. **Thu thập dữ liệu mới (New Data Collection)**:
   - Thu thập dữ liệu giao dịch mới từ nhiều sàn giao dịch tiền mã hóa như Binance, Coinbase, KuCoin, và Kraken.

5. **Xử lý dữ liệu mới (New Data Processing)**:
   - Làm sạch và chuẩn bị dữ liệu mới để áp dụng mô hình.

6. **Áp dụng mô hình (Apply Model to New Data)**:
   - Áp dụng mô hình đã huấn luyện để dự đoán giao dịch gian lận trên tập dữ liệu mới.

---

## Cấu Trúc Dự Án

Dự án bao gồm các tệp Jupyter Notebook sau:

### 1. **`old_data_processing.ipynb`**
- **Mục tiêu**: Làm sạch, chuẩn hóa, và cân bằng dữ liệu cũ.
- **Các bước chính**:
  - Đọc và khám phá dữ liệu ban đầu.
  - Loại bỏ dữ liệu bị lỗi hoặc không cần thiết.
  - Chuẩn hóa dữ liệu về định dạng phù hợp.
  - Sử dụng **SMOTE** để tạo thêm dữ liệu cho nhãn "gian lận" (nhãn thiểu số) nhằm cân bằng dữ liệu.
- **Kết quả**: Tạo ra tập dữ liệu sạch và cân bằng để chuẩn bị cho bước huấn luyện.

---

### 2. **`train_validation_split.ipynb`**
- **Mục tiêu**: Chia dữ liệu thành các tập huấn luyện, kiểm tra và xác thực.
- **Các bước chính**:
  - Sử dụng thư viện **sklearn** để chia dữ liệu.
  - Đảm bảo phân phối nhãn giữa các tập được cân bằng.
- **Kết quả**: Các tập dữ liệu được lưu lại để sử dụng trong quá trình huấn luyện.

---

### 3. **`ann_training.ipynb`**
- **Mục tiêu**: Huấn luyện mô hình mạng nơ-ron nhân tạo (ANN) để trích xuất đặc trưng từ dữ liệu.
- **Các bước chính**:
  - Xây dựng mô hình ANN với thư viện **Keras**.
  - Huấn luyện mô hình trên tập dữ liệu huấn luyện.
  - Lưu lại mô hình đã huấn luyện để sử dụng trong các bước tiếp theo.
- **Kết quả**: Mô hình ANN đã được huấn luyện và sẵn sàng để sử dụng.

---

### 4. **`svm_training.ipynb`**
- **Mục tiêu**: Sử dụng SVM để phân loại dựa trên đặc trưng từ ANN.
- **Các bước chính**:
  - Lấy các đặc trưng từ ANN.
  - Huấn luyện mô hình SVM trên các đặc trưng này.
  - Đánh giá hiệu suất mô hình SVM với các số liệu như ma trận nhầm lẫn, độ chính xác, độ nhạy.
- **Kết quả**: Mô hình SVM đã được huấn luyện để thực hiện phân loại.

---

### 5. **`new_data_collection.ipynb`**
- **Mục tiêu**: Thu thập dữ liệu giao dịch mới từ các sàn giao dịch tiền mã hóa.
- **Các bước chính**:
  - Sử dụng API từ các sàn như Binance, Coinbase, KuCoin, Kraken để lấy dữ liệu.
  - Thu thập dữ liệu từ khoảng 20 cặp giao dịch chính trên mỗi sàn.
  - Lưu trữ dữ liệu dưới định dạng CSV.
- **Kết quả**: Bộ dữ liệu giao dịch mới từ nhiều sàn được lưu trữ và sẵn sàng cho tiền xử lý.

---

### 6. **`new_data_processing.ipynb`**
- **Mục tiêu**: Tiền xử lý dữ liệu mới để chuẩn bị cho mô hình.
- **Các bước chính**:
  - Làm sạch dữ liệu mới, loại bỏ giá trị thiếu hoặc không hợp lệ.
  - Chuẩn hóa các cột và thêm các đặc trưng như biến động giá (price volatility).
- **Kết quả**: Tập dữ liệu mới được làm sạch và sẵn sàng cho dự đoán.

---

### 7. **`apply_model_to_new_data.ipynb`**
- **Mục tiêu**: Áp dụng mô hình đã huấn luyện lên tập dữ liệu mới.
- **Các bước chính**:
  - Tải mô hình ANN và SVM đã huấn luyện.
  - Dự đoán nhãn "gian lận" hoặc "không gian lận" trên tập dữ liệu mới.
  - Phân tích và đánh giá kết quả dự đoán.
- **Kết quả**: Kết quả dự đoán được lưu lại để phân tích.

---

## Lợi Ích Nghiên Cứu

1. **Góp phần chống gian lận tài chính**: Dự án cung cấp một giải pháp thực tiễn để phát hiện gian lận trong các giao dịch tiền mã hóa.
2. **Ứng dụng công nghệ hiện đại**: Kết hợp ANN và SVM cho phép tận dụng điểm mạnh của cả hai mô hình.
3. **Cải thiện hiểu biết về giao dịch tài chính**: Phân tích các đặc trưng giao dịch giúp hiểu rõ hơn về hành vi người dùng.

---

## Yêu Cầu Môi Trường

- Python >= 3.8
- Các thư viện cần thiết:
  - `tensorflow`
  - `scikit-learn`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `imbalanced-learn`

---

## Hướng Dẫn Sử Dụng

1. Chạy các tệp notebook theo thứ tự:
   - `old_data_processing.ipynb`
   - `train_validation_split.ipynb`
   - `ann_training.ipynb`
   - `svm_training.ipynb`
   - `new_data_collection.ipynb`
   - `new_data_processing.ipynb`
   - `apply_model_to_new_data.ipynb`

2. Kiểm tra kết quả dự đoán và phân tích dữ liệu đầu ra từ mô hình.

---

## Tác Giả

- **Người thực hiện**: Nguyễn Đình Khải _ Nhóm 9

---

## Ghi Chú