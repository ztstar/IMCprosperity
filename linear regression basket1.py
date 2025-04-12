from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error

# 读数据
df1 = pd.read_csv("prices_round_2_day_-1.csv")
df2 = pd.read_csv("prices_round_2_day_0.csv")
df3 = pd.read_csv("prices_round_2_day_1.csv")
df = pd.concat([df1, df2, df3])

PICNIC_BASKET1 = []
Croissants = []
Jams = []
Djemebes = []

last_time_stamp = ""
CROISSANTS_PRICE = ""
JAMS_PRICE = ""
PICNIC_BASKET1_PRICE = ""
DJEMBES_PRICE = ""

# 提取价格
for index, row in df.iterrows():
    raw_str = row.iloc[0]
    parts = raw_str.split(';')
    
    if last_time_stamp != parts[1]:
        cnt = 0
    last_time_stamp = parts[1]
    
    if parts[2] == "CROISSANTS":
        CROISSANTS_PRICE = parts[15]
        cnt += 1
    if parts[2] == "JAMS":
        JAMS_PRICE = parts[15]
        cnt += 1
    if parts[2] == "PICNIC_BASKET1":
        PICNIC_BASKET1_PRICE = parts[15]
        cnt += 1
    if parts[2] == "DJEMBES":
        DJEMBES_PRICE = parts[15]
        cnt += 1

    # print(cnt)

    if cnt == 4:
        PICNIC_BASKET1.append(float(PICNIC_BASKET1_PRICE))
        Croissants.append(float(CROISSANTS_PRICE))
        Jams.append(float(JAMS_PRICE))
        Djemebes.append(float(DJEMBES_PRICE))

# 构造 X: Jams^2 和 Croissants^2
Jams = np.array(Jams)
Croissants = np.array(Croissants)
Djemebes = np.array(Djemebes)

X = np.column_stack((Jams, Croissants, Djemebes))

# print(X)

# 拟合模型
model = LinearRegression()
model.fit(X, PICNIC_BASKET1)

print("Intercept (b0):", model.intercept_)
print("Coefficients (b1 for Jams, b2 for Croissants, b3 for Djemebes):", model.coef_)

# 预测 + 残差
y_pred = model.predict(X)
residuals = np.array(PICNIC_BASKET1) - y_pred


# 残差分布图
plt.figure(figsize=(8, 4))
sns.histplot(residuals, kde=True, bins=30, color="skyblue")
plt.title("Distribution of Residuals")
plt.xlabel("Residual Value")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# ADF test
adf_result = adfuller(residuals)
print("ADF Statistic:", adf_result[0])
print("p-value:", adf_result[1])
if adf_result[1] < 0.05:
    print("OK")
else:
    print("NOT OK")

# MSE
mse = mean_squared_error(PICNIC_BASKET1, y_pred)
print("mse = ", mse)

# 实际 vs 预测
plt.figure(figsize=(10, 5))
plt.plot(PICNIC_BASKET1, label='Actual', marker='o')
plt.plot(y_pred, label='Predicted', marker='x')
plt.title("Actual vs Predicted PICNIC_BASKET2 Prices")
plt.legend()
plt.grid(True)
plt.show()

# 将 y 转为 NumPy 数组
y = np.array(PICNIC_BASKET1)

# 计算下5%和上95%分位数
lower_bound = np.percentile(residuals, 5)
upper_bound = np.percentile(residuals, 95)

print("5th percentile:", lower_bound)
print("95th percentile:", upper_bound)