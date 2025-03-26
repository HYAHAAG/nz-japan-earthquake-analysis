import requests
import pandas as pd
from datetime import datetime

# 保存先をEドライブに
output_path = "E:/earthquake_analysis_nz_japan/nz_earthquakes.csv"

# USGS Earthquake API エンドポイント
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# ニュージーランド周辺の地震（緯度・経度・期間）
params = {
    "format": "geojson",
    "starttime": "2000-01-01",
    "endtime": "2024-12-31",
    "minlatitude": -50,
    "maxlatitude": -30,
    "minlongitude": 160,
    "maxlongitude": 180,
    "minmagnitude": 6.5,
    "orderby": "time-asc",
    "limit": 20000  # 最大件数
}

# データ取得
response = requests.get(url, params=params)
data = response.json()

# 必要な情報だけ抽出
records = []
for feature in data["features"]:
    props = feature["properties"]
    coords = feature["geometry"]["coordinates"]
    records.append({
        "time": props["time"],
        "place": props["place"],
        "mag": props["mag"],
        "longitude": coords[0],
        "latitude": coords[1],
        "depth": coords[2]
    })

# DataFrameに変換
df = pd.DataFrame(records)
df["time"] = pd.to_datetime(df["time"], unit="ms")

# CSVに保存
df.to_csv(output_path, index=False)
print(f"✅ Saved {len(df)} earthquake records to {output_path}")
