import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

data_dir = "../data/old_data/processed/data_processed.csv"
data = pd.read_csv(data_dir)

# Chọn các đặc trưng để phát hiện bất thường
features = ["Open", "High", "Low", "Close", "Volume", "Price_Change_Pct", "Volume_Spike", "Volatility"]

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[features])

# Isolation Forest với contamination ~0.01 (tỷ lệ bất thường ~1%)
iso_forest = IsolationForest(contamination=0.01, random_state=42)
data['Anomaly_Score'] = iso_forest.fit_predict(data_scaled)

# Gắn nhãn: -1 là bất thường, 1 là bình thường
data['Label'] = (data['Anomaly_Score'] == -1).astype(int)

print("Phân phối nhãn bất thường sau Isolation Forest:")
print(data['Label'].value_counts())
