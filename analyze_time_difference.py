import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter

# 日本語フォント対応（任意）
matplotlib.rcParams['font.family'] = 'Yu Gothic'

# ファイル読み込み
nz_df = pd.read_csv("E:/earthquake_analysis_nz_japan/nz_earthquakes.csv", parse_dates=["time"])
jp_df = pd.read_csv("E:/earthquake_analysis_nz_japan/japan_earthquakes.csv", parse_dates=["time"])

# 時間差（日）を保存するリスト
day_differences = []

# 分析する最大日数（例：30日後まで）
max_days = 30

for nz_time in nz_df["time"]:
    # NZ地震から30日以内に起きた日本の地震を抽出
    matches = jp_df[(jp_df["time"] > nz_time) & (jp_df["time"] <= nz_time + timedelta(days=max_days))]

    for jp_time in matches["time"]:
        delta_days = (jp_time - nz_time).days
        day_differences.append(delta_days)

# 日数ごとの件数をカウントして出力
counter = Counter(day_differences)
print("NZ地震からの日数ごとの地震件数：")
for day in sorted(counter.keys()):
    print(f"{day}日後: {counter[day]}件")


# ヒストグラムで分布を表示
plt.hist(day_differences, bins=range(1, max_days + 1), align="left", rwidth=0.8)
plt.xlabel("NZ地震からの日数")
plt.ylabel("日本での地震件数")
plt.title("NZ地震後、日本での地震発生までの日数分布")
plt.tight_layout()
plt.savefig("E:/earthquake_analysis_nz_japan/nz_japan_day_difference_hist.png")
plt.show()

