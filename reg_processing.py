import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def clean(value):
    s1 = value.split('[')
    s2 = s1[1].split(']')
    return float(s2[0])

df = pd.read_csv('balance_deviation.csv', sep=',')
df2 = pd.read_csv('data_balances.csv', sep=',')

Xbal = []
for i in range(0, len(df2)):
    Xbal.append(df2.Balances[i])

rawBalanceGrowthMetrics = []
count = 0
for balance in Xbal:
    print(count.__str__()+"/"+len(Xbal).__str__())
    values = []
    for i in range(0, len(df)):
        if balance == df.Balance[i]:
            values.append(df.Deviation[i])
    rawBalanceGrowthMetrics.append((balance, values))
    count += 1

balanceGrowthMetrics = []
for balance, l in rawBalanceGrowthMetrics:
    count = 0
    px = []
    py = []
    for val in l:
        px.append(clean(val))
        py.append(count)
        count+=1
    if(len(px) > 1):
        x = np.array(px).reshape((-1,1))
        y = np.array(py)
        model = LinearRegression().fit(x, y)
        if(len(px) >= 10):
            balanceGrowthMetrics.append((balance, model.coef_[0], model.score(x,y), len(px)))
        else:
            balanceGrowthMetrics.append((balance, model.coef_[0], 1, len(px)))

l1 = []
l2 = []
l3 = []
l4 = []
for balance, coef, score, nbItems in balanceGrowthMetrics:
    l1.append(balance)
    l2.append(coef)
    l3.append(score)
    l4.append(nbItems)


zipped = list(zip(l1, l2, l3, l4))
data = pd.DataFrame(zipped, columns=['Balance', 'Deviation', 'Precision', 'Nb_Entrees'])

data.to_csv('balance_deviation_rate.csv')

