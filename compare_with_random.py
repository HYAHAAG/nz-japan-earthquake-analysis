import pandas as pd
import numpy as np
from datetime import timedelta
from scipy.stats import fisher_exact
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Yu Gothic'  # WindowsならYu Gothicがおすすめ


# データ読み込み
nz_df = pd.read_csv("E:/earthquake_analysis_nz_japan/nz_earthquakes.csv", parse_dates=["time"])
jp_df = pd.read_csv("E:/earthquake_analysis_nz_japan/japan_earthquakes.csv", parse_dates=["time"])

# 日本の地震日リスト
jp_dates = jp_df["time"]

# 検証する日数リスト
day_ranges = [7, 14, 21]

# 結果格納
results = []

for days in day_ranges:
    # NZ地震日ごとのチェック
    nz_success = 0
    for nz_time in nz_df["time"]:
        end_time = nz_time + timedelta(days=days)
        if not jp_dates[(jp_dates >= nz_time) & (jp_dates <= end_time)].empty:
            nz_success += 1

    # ランダムな日（NZ地震と同じ件数）
    random_success = 0
    start_date = jp_df["time"].min()
    end_date = jp_df["time"].max()
    random_dates = pd.to_datetime(np.random.choice(pd.date_range(start_date, end_date), size=len(nz_df), replace=False))

    for rand_time in random_dates:
        end_time = rand_time + timedelta(days=days)
        if not jp_dates[(jp_dates >= rand_time) & (jp_dates <= end_time)].empty:
            random_success += 1

    # 有意差検定（Fisherの正確確率検定）
    table = [[nz_success, len(nz_df) - nz_success],
             [random_success, len(nz_df) - random_success]]
    _, p_value = fisher_exact(table)

    # 結果を保存
    results.append({
        "期間（日）": days,
        "NZ地震後の日本地震回数": nz_success,
        "ランダム日の日本地震回数": random_success,
        "p値": round(p_value, 4)
    })

# 結果表示
result_df = pd.DataFrame(results)
print(result_df)

# 可視化
x = result_df["期間（日）"]
nz_vals = result_df["NZ地震後の日本地震回数"]
rand_vals = result_df["ランダム日の日本地震回数"]

width = 2
plt.bar(x - width/2, nz_vals, width=width, label="NZ地震後")
plt.bar(x + width/2, rand_vals, width=width, label="ランダム日")
plt.xlabel("期間（日）")
plt.ylabel("日本での地震回数")
plt.title("NZ地震 vs ランダムな日：日本地震発生比較")
plt.legend()
plt.tight_layout()
plt.savefig("E:/earthquake_analysis_nz_japan/comparison_plot.png")
plt.show()
