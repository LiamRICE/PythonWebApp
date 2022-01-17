import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv('raw_data_balances_sorted.csv', sep=',')
df2 = pd.read_csv('data_balances.csv', sep=',')

Xbal = []
#for i in range(0, len(df2)):
for i in range(0, 100):
    Xbal.append(df2.Balances[i])

print("Sorting data from csv...")
arrayByBalanceAndByTimeBetweenExceptions = []
count = 1
for balance in Xbal:
    print(count.__str__()+"/"+len(Xbal).__str__())
    tempBalList = []
    tempExpList = []
    for i in range(0, len(df)):
        if df.Balance[i] == balance:
            if df.TARException[i] == 1:
                tempExpList.append((df.Balance[i], df.MeasuredWeight[i], df.Weight[i], df.Date[i]))
                tempBalList.append(tempExpList)
                tempExpList = []
            else:
                tempExpList.append((df.Balance[i], df.MeasuredWeight[i], df.Weight[i], df.Date[i]))
    tempBalList.append(tempExpList)
    arrayByBalanceAndByTimeBetweenExceptions.append(tempBalList)
    count += 1
print("Done.")

print("Resetting data...")
arrayOfWeightDivergence = []
for balanceList in arrayByBalanceAndByTimeBetweenExceptions:
    balanceDivergence = []
    for exeptionList in balanceList:
        expDivergence = []
        for b, measuredWeight, weight, date in exeptionList:
            expDivergence.append((b, measuredWeight, date))
        balanceDivergence.append(expDivergence)
    arrayOfWeightDivergence.append(balanceDivergence)
print("Done.")

print("Calculating Linear Regression...")
linearRegressionByBalance = []
for balList in arrayOfWeightDivergence:
    linearB = []
    balance = ""
    for expList in balList:
        pick = 0
        px = []
        py = []
        for b, weight, date in expList:
            px.append(pick)
            py.append(weight)
            balance = b
            pick += 1
        x = np.array(px).reshape((-1,1))
        y = np.array(py)
        if(len(px)>1):
            model = LinearRegression().fit(x, y)
            if(len(px) >= 10):
                linearB.append((model.coef_, model.score(x,y)))
            else:
                linearB.append((model.coef_, 1))
    linearRegressionByBalance.append((balance, linearB))
print("Done.")

l1 = []
l2 = []
l3 = []
for balance, line in linearRegressionByBalance:
    for coef, score in line:
        l1.append(balance)
        l2.append(coef)
        l3.append(score)


zipped = list(zip(l1, l2, l3))
data = pd.DataFrame(zipped, columns=['Balance', 'Deviation', 'Precision'])

data.to_csv('balance_deviation.csv')

    
    



