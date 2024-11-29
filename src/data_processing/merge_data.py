import os
import pandas as pd
from src.data_processing.clean_data import clean_data


def merge_and_clean_data(raw_dir, processed_file):
    all_data = []

    # Duyệt qua các thư mục của từng sàn
    for exchange in os.listdir(raw_dir):
        exchange_dir = os.path.join(raw_dir, exchange)
        if os.path.isdir(exchange_dir):
            for file in os.listdir(exchange_dir):
                file_path = os.path.join(exchange_dir, file)
                if file.endswith('.csv'):
                    print(f"Đọc file: {file_path}")
                    df = pd.read_csv(file_path)

                    # Làm sạch dữ liệu
                    df = clean_data(df)

                    # Thêm cột nhận diện sàn giao dịch
                    df['exchange'] = exchange

                    all_data.append(df)

    # Gộp tất cả dữ liệu
    combined_df = pd.concat(all_data, ignore_index=True)

    # Lưu dữ liệu đã xử lý
    combined_df.to_csv(processed_file, index=False)
    print(f"Dữ liệu đã được lưu tại: {processed_file}")
