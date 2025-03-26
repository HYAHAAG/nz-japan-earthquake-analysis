import pandas as pd
from datetime import timedelta

# ファイル読み込み
nz_df = pd.read_csv("E:/earthquake_analysis_nz_japan/nz_earthquakes.csv", parse_dates=["time"])
jp_df = pd.read_csv("E:/earthquake_analysis_nz_japan/japan_earthquakes.csv", parse_dates=["time"])

# 何日以内に起きたかをチェック（7日）
days_within = 14
count = 0
match_dates = []

for nz_time in nz_df["time"]:
    start = nz_time
    end = nz_time + timedelta(days=days_within)

    # この期間内に日本で地震があるか
    match = jp_df[(jp_df["time"] >= start) & (jp_df["time"] <= end)]
    if not match.empty:
        count += 1
        match_dates.append((nz_time.strftime("%Y-%m-%d"), len(match)))

# 結果表示
print(f"✅ NZの大地震のうち、{days_within}日以内に日本でも地震があった回数：{count} / {len(nz_df)}")
print("⚡ 対応した日付一覧：")
for date, num in match_dates:
    print(f"- {date} → 日本で {num} 件")
