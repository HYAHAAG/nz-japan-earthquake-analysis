import pandas as pd
from scipy.stats import fisher_exact

# データ読み込み
nz_df = pd.read_csv("E:/earthquake_analysis_nz_japan/nz_earthquakes.csv", parse_dates=["time"])
jp_df = pd.read_csv("E:/earthquake_analysis_nz_japan/japan_earthquakes.csv", parse_dates=["time"])

# NZ地震ごとに、17日後に日本で地震が1件以上あったかどうかを確認
nz_with_17day = 0
nz_without_17day = 0

for nz_time in nz_df["time"]:
    day_17_start = nz_time + pd.Timedelta(days=17)
    day_17_end = day_17_start + pd.Timedelta(days=1)

    # 17日後の0:00〜23:59に日本で地震があったかを確認
    match = jp_df[(jp_df["time"] >= day_17_start) & (jp_df["time"] < day_17_end)]
    if not match.empty:
        nz_with_17day += 1
    else:
        nz_without_17day += 1

# 結果表示
print("✅ NZで17日後に日本で地震があった件数:", nz_with_17day)
print("✅ NZで17日後に日本で地震がなかった件数:", nz_without_17day)

# Fisher検定（こっちのほうが安全）
table = [[nz_with_17day, nz_without_17day]]
_, p = fisher_exact(table)

print(f"📊 Fisherの正確確率検定のp値: {p:.5f}")
if p < 0.05:
    print("✅ 有意差あり！偶然とは考えにくい集中です。")
else:
    print("⚠️ 有意差なし（偶然の可能性も高いです）")
