import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
# --- 1. Synthetic Data Generation ---
np.random.seed(42)  # for reproducibility
dates = pd.date_range(start='2022-01-01', periods=365)
bounce_rate = 0.4 + 0.1 * np.sin(2 * np.pi * np.arange(365) / 365) + 0.05 * np.random.randn(365) #Seasonal trend + noise
external_events = [0] * 365
external_events[100] = 1 # Simulate a marketing campaign
external_events[200] = -0.5 # Simulate a website issue
bounce_rate += 0.05 * np.array(external_events)
df = pd.DataFrame({'Date': dates, 'BounceRate': bounce_rate})
# --- 2. Time Series Decomposition ---
decomposition = seasonal_decompose(df['BounceRate'], model='additive', period=30) # Adjust period as needed
# --- 3. Augmented Dickey-Fuller Test for Stationarity ---
result = adfuller(df['BounceRate'])
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))
# --- 4. Visualization ---
# Plot the original time series
plt.figure(figsize=(12, 8))
plt.plot(df['Date'], df['BounceRate'], label='Original Bounce Rate')
plt.title('Website Bounce Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Bounce Rate')
plt.legend()
# Plot the decomposed components
plt.figure(figsize=(12, 8))
plt.subplot(411)
plt.plot(decomposition.observed, label='Observed')
plt.legend()
plt.subplot(412)
plt.plot(decomposition.trend, label='Trend')
plt.legend()
plt.subplot(413)
plt.plot(decomposition.seasonal, label='Seasonal')
plt.legend()
plt.subplot(414)
plt.plot(decomposition.resid, label='Residual')
plt.legend()
plt.tight_layout()
# Save plots
plt.savefig('bounce_rate_decomposition.png')
print("Plot saved to bounce_rate_decomposition.png")
plt.figure(figsize=(10,6))
plt.plot(df['Date'],df['BounceRate'])
plt.title('Bounce Rate with External Events')
plt.xlabel('Date')
plt.ylabel('Bounce Rate')
plt.scatter(df['Date'][external_events != 0], df['BounceRate'][external_events != 0], color='red', label='External Events')
plt.legend()
plt.savefig('bounce_rate_external_events.png')
print("Plot saved to bounce_rate_external_events.png")