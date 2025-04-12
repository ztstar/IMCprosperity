from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

df1 = pd.read_csv("prices_round_2_day_-1.csv")
df2 = pd.read_csv("prices_round_2_day_0.csv")
df3 = pd.read_csv("prices_round_2_day_1.csv")
df = pd.concat([df1, df2, df3])

# print(df.head(df))

PICNIC_BASKET2 = []

Croissants = []

Jams = []

last_time_stamp = ""
CROISSANTS_PRICE = ""
JAMS_PRICE = ""
PICNIC_BASKET2_PRICE = ""

for index, row in df.iterrows():
    raw_str = row.iloc[0]
    parts = raw_str.split(';')
    # print(len(parts))
    # print(parts[2], parts[15])
    # print(type(parts[2]), type(parts[15]))
    if last_time_stamp != parts[1]:
        cnt = 0
    # print(last_time_stamp, parts[1])
    last_time_stamp = parts[1]
    if parts[2] == "CROISSANTS":
        CROISSANTS_PRICE = parts[15]
        cnt += 1
    if parts[2] == "JAMS":
        JAMS_PRICE = parts[15]
        cnt += 1
    if parts[2] == "PICNIC_BASKET2":
        PICNIC_BASKET2_PRICE = parts[15]
        cnt += 1
    # print(cnt)
    if cnt == 3:
        PICNIC_BASKET2.append(float(PICNIC_BASKET2_PRICE))
        Croissants.append(float(CROISSANTS_PRICE))
        Jams.append(float(JAMS_PRICE))

# print(Croissants)

X = np.column_stack((Jams, Croissants))

# print(X)

model = LinearRegression()
model.fit(X, PICNIC_BASKET2)

print("Intercept (b0):", model.intercept_)
print("Coefficients (b1, b2):", model.coef_)

y_pred = model.predict(X)

residuals = np.array(PICNIC_BASKET2) - y_pred

from statsmodels.tsa.stattools import adfuller

adf_result = adfuller(residuals)

print("ADF Statistic:", adf_result[0])
print("p-value:", adf_result[1])

if adf_result[1] < 0.05:
    print("OK")
else:
    print("NOT OK")

from sklearn.metrics import mean_squared_error

mse = mean_squared_error(PICNIC_BASKET2, y_pred)
print("mse = ", mse)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(PICNIC_BASKET2, label='Actual', marker='o')
plt.plot(y_pred, label='Predicted', marker='x')
plt.title("Actual vs Predicted PICNIC_BASKET2 Prices")
plt.legend()
plt.grid(True)
plt.show()


