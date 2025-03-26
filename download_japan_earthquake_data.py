import requests
import pandas as pd
from datetime import datetime

# 保存先
output_path = "E:/earthquake_analysis_nz_japan/japan_earthquakes.csv"

# USGS APIエンドポイント
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# 日本周辺の地震（緯度・経度・期間）
params = {
    "format": "geojson",
    "starttime": "2000-01-01",
    "endtime": "2024-12-31",
    "minlatitude": 30,
    "maxlatitude": 46,
    "minlongitude": 129,
    "maxlongitude": 146,
    "minmagnitude": 6.0,
    "orderby": "time-asc",
    "limit": 20000
}

# データ取得
response = requests.get(url, params=params)
data = response.json()

# 必要な情報を抽出
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
