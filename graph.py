import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("scoresData.csv", header=None)

values = []
for i in range(0, data.shape[0]):
	values.append(data.iloc[i,:].quantile([0,0.25,0.5,0.75,1]).values)


plt.plot(values)
plt.legend(["0th Percentile", "25th Percentile", "50th Percentile", "75th Percentile", "100th Percentile"])
plt.show()

