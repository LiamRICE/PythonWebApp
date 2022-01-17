import pandas as pd

print("Loading...")
df_balances = pd.read_csv("data_balances.csv", ",")
print("Done.")

print("Processing...")
balanceList = []
missionsList = []
exceptionList = []
weightList = []
negList = []
for i in range(0, len(df_balances)):
    balanceList.append(df_balances.Balances[i])
    missionsList.append(df_balances.NumMissions[i])
    exceptionList.append(df_balances.ExceptionRate[i])
    weightList.append(df_balances.AvgWeightDiff[i])
    if(df_balances.NumMissions[i] != 0):
        negList.append(df_balances.NumNegativeWeights[i] / df_balances.NumMissions[i])
    else:
        negList.append(0)
print("Done.")

print("Loading to csv...")
zipped = list(zip(balanceList, missionsList, exceptionList))
TAR_data = pd.DataFrame(zipped, columns=['Balance','Missions','TARExceptionRate'])
zipped = list(zip(balanceList, missionsList, weightList))
weight_data = pd.DataFrame(zipped, columns=['Balance','Missions','AverageWeightDiff'])
zipped = list(zip(balanceList, missionsList, negList))
neg_data = pd.DataFrame(zipped, columns=['Balance','Missions','NegativeWeightRate'])
zipped = list(zip(balanceList, exceptionList, weightList, negList))
balDF = pd.DataFrame(zipped, columns=['Balance','ExceptionRate','WeightDiff','NegRate'])
TAR_data.to_csv('tar_data_balances.csv')
weight_data.to_csv('weight_data_balances.csv')
neg_data.to_csv('neg_data_balances.csv')
balDF.to_csv('balance_all_val.csv')
print("End.")