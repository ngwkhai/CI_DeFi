import pandas as pd
import numpy as np


def clean_data(df):
    # Chuyển đổi cột thời gian
    df['time'] = pd.to_datetime(df['time'], errors='coerce')

    # Loại bỏ các dòng có giá trị thời gian không hợp lệ
    df = df.dropna(subset=['time'])

    # Chuyển các cột giá và khối lượng về kiểu số
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Loại bỏ các dòng có giá trị thiếu hoặc không hợp lệ
    df = df.dropna()

    # Đảm bảo dữ liệu được sắp xếp theo thời gian
    df = df.sort_values(by='time').reset_index(drop=True)

    return df
