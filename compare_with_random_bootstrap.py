import pandas as pd
import numpy as np
from datetime import timedelta
from scipy.stats import fisher_exact
import matplotlib.pyplot as plt
import matplotlib

# 日本語フォント対策
matplotlib.rcParams['font.family'] = 'Yu Gothic'

# データ読み込み
nz_df = pd.read_csv("E:/earthquake_analysis_nz_japan/nz_earthquakes.csv", parse_dates=["time"])
jp_df = pd.read_csv("E:/earthquake_analysis_nz_japan/japan_earthquakes.csv", parse_dates=["time"])
jp_dates = jp_df["time"]

# 検証する日数
day_ranges = [7, 14, 21]
num_bootstraps = 100

results = []

for days in day_ranges:
    nz_success = 0
    for nz_time in nz_df["time"]:
        end = nz_time + timedelta(days=days)
        if not jp_dates[(jp_dates >= nz_time) & (jp_dates <= end)].empty:
            nz_success += 1

    # ランダムセット100回実行
    random_counts = []
    start_date = jp_df["time"].min()
    end_date = jp_df["time"].max()

    for _ in range(num_bootstraps):
        rand_dates = pd.to_datetime(np.random.choice(pd.date_range(start_date, end_date), size=len(nz_df), replace=False))
        rand_success = 0
        for rand_time in rand_dates:
            rand_end = rand_time + timedelta(days=days)
            if not jp_dates[(jp_dates >= rand_time) & (jp_dates <= rand_end)].empty:
                rand_success += 1
        random_counts.append(rand_success)

    # p値（NZ成功回数 vs ランダム平均成功回数）
    avg_random = np.mean(random_counts)
    table = [[nz_success, len(nz_df) - nz_success], [avg_random, len(nz_df) - avg_random]]
    _, p_value = fisher_exact(table)

    results.append({
        "期間（日）": days,
        "NZ成功数": nz_success,
        "ランダム平均成功数": round(avg_random, 2),
        "p値": round(p_value, 4)
    })

    # グラフ描画（各日数ごと）
    plt.hist(random_counts, bins=15, alpha=0.6, label="ランダムな日")
    plt.axvline(nz_success, color='red', linestyle='--', label=f"NZ地震後（{nz_success}件）")
    plt.title(f"{days}日以内の日本地震件数比較")
    plt.xlabel("日本での地震件数")
    plt.ylabel("ランダム日セットの頻度")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"E:/earthquake_analysis_nz_japan/random_bootstrap_{days}days.png")
    plt.clf()

# 表形式で出力
result_df = pd.DataFrame(results)
print(result_df)
