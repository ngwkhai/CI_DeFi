import pandas as pd
import numpy as np


def add_features(df):
    # Tính toán biến động giá (volatility)
    df['log_return'] = np.log(df['close'] / df['close'].shift(1))
    df['volatility'] = df['log_return'].rolling(window=20).std()

    # Tính toán khối lượng giao dịch tăng đột biến (Volume Spike)
    df['avg_volume'] = df['volume'].rolling(window=20).mean()
    df['volume_spike'] = df['volume'] > (2.0 * df['avg_volume'])

    # Tạo cột mục tiêu (label): 1 nếu có Pump and Dump, 0 nếu không
    df['pump_and_dump'] = (df['volatility'] > 0.02) & (df['volume_spike'] == True)
    df['pump_and_dump'] = df['pump_and_dump'].astype(int)

    return df
