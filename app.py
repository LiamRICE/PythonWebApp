# app
import dash
from dash import dash_table
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

print("Reading raw data...")
df = pd.read_csv('data_balea.csv', sep=';')
newDF = pd.read_csv('data_trucks.csv', sep=',')
figDF = pd.read_csv('data_fig.csv', sep=',')
#new csv regarding balances
balancesDF = pd.read_csv('data_balances.csv', sep=",")
balancesDeviationDF = pd.read_csv('balance_deviation.csv', sep=",")
balancesDeviationRate = pd.read_csv("balance_deviation_rate.csv",sep=",")
negWeightDF = pd.read_csv("neg_data_balances.csv",sep=",")
tarBalancesDF = pd.read_csv("tar_data_balances.csv", sep=",")
print("Data read.")

list1 = []
list2 = []
list3 = []
for i in range(0, len(newDF)):
    if newDF.ExceptionRate[i] >= 0.06 and newDF.NumMissions[i] >= 1000:
        list1.append(newDF.Trucks[i])
        list2.append(newDF.ExceptionRate[i])
        list3.append(newDF.NumNegativeWeights[i])
zipped = list(zip(list1, list2, list3))
fig2DF = pd.DataFrame(zipped, columns=['Trucks', 'TARExceptions', 'NumNegativeWeights'])

# make figure
fig = px.scatter(figDF, x="missions", y="exceptions", color="names", hover_name="names", log_x=True)
fig2 = px.bar(fig2DF, x="Trucks", y="NumNegativeWeights", color="Trucks", hover_name="Trucks")

# new figure
balancesFigure = px.scatter(balancesDF,x="NumMissions", y="AvgWeightDiff", color="Balances")
negWeightBalances = px.scatter(negWeightDF,x="Missions", y="NegativeWeightRate", color="Balance")
tarExceptionBalances = px.scatter(tarBalancesDF,x="Missions", y="TARExceptionRate", color="Balance")


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Balea Data Analysis'),

    dcc.Tabs([
                dcc.Tab(label='Analysis', children=[
            dcc.Tabs([
                dcc.Tab(label='Difference between theory weight and observed weight Analysis', children=[
                    dcc.Graph(
                id='data-graph-balance-weight-diff',
                figure=balancesFigure
            ),
                        dcc.Slider(
                id='threshold-difference-weight',
                min=0,
                max=1.1,
                step=0.01,
                value=0

            ),
            html.Div(id='slider-output-difference-weight')
                ]),
                
                dcc.Tab(label='Negative Rate Per Balance Analysis', children=[
                    dcc.Graph(
                id='data-graph-negative-rate',
                figure=negWeightBalances
            ),
            dcc.Slider(
                id='threshold-negative-rate',
                min=0,
                max=0.10,
                step=0.01,
                value=0

            ),
            html.Div(id='slider-output-container')
                ]),
                dcc.Tab(label='TAR Exception Per Balance Analysis', children=[
                    dcc.Graph(
                id='data-graph-tar-exception',
                figure=tarExceptionBalances
            ),

            dcc.Slider(
                id='threshold-tar-exception-rate',
                min=0,
                max=0.15,
                step=0.01,
                value=0

            ),
            html.Div(id='slider-output-tar-exception-rate')
                ]),
            ])
        ]),
        dcc.Tab(label='Data', children=[
            dcc.Tabs([
                dcc.Tab(label='Raw Data', children=[
                    html.Div(children='''
                        Header table of the raw data.
                    '''),
                    dash_table.DataTable(
                    id = 'table-head',
                    columns = [{"name":i, "id":i} for i in df.columns],
                    data = df.to_dict('records'),
                    page_size=50
                    )
                ]),

                dcc.Tab(label='Truck Data', children=[
                    html.Div(children='''
                        Synthesised table of data for each truck.
                    '''),
                    dash_table.DataTable(
                    id = 'new-table',
                    columns = [{"name":i, "id":i} for i in newDF.columns],
                    data = newDF.to_dict('records')
                    )
                ]),
                
                dcc.Tab(label='Exceptions Graph', children=[
                    dcc.Graph(
                        id='graph-of-new-data',
                        figure=fig
                    )
                ]),
            ])
        ]),

    ])
])

#Negative Rate Per Balance Slider
@app.callback(
dash.dependencies.Output('data-graph-negative-rate', 'figure'),
[dash.dependencies.Input('threshold-negative-rate', 'value')])
def update_negative_rate_threshold(threshold):
    filtered_df = negWeightDF[negWeightDF.NegativeWeightRate>threshold]
    filtered_negWeightBalances = px.scatter(filtered_df,x="Missions", y="NegativeWeightRate", color="Balance")
    filtered_negWeightBalances.update_layout(transition_duration=500)
    return filtered_negWeightBalances

@app.callback(
dash.dependencies.Output('slider-output-container', 'children'),
[dash.dependencies.Input('threshold-negative-rate', 'value')])
def update_output(value):
    return 'Threshold selected "{}"'.format(value)


#Difference weight Per Balance Slider
@app.callback(
dash.dependencies.Output('data-graph-balance-weight-diff', 'figure'),
[dash.dependencies.Input('threshold-difference-weight', 'value')])
def update_negative_rate_threshold(threshold):
    filtered_df = balancesDF[balancesDF.AvgWeightDiff>threshold]
    filtered_balancesFigure = px.scatter(filtered_df,x="NumMissions", y="AvgWeightDiff", color="Balances")
    filtered_balancesFigure.update_layout(transition_duration=500)
    return filtered_balancesFigure

@app.callback(
dash.dependencies.Output('slider-output-difference-weight', 'children'),
[dash.dependencies.Input('threshold-difference-weight', 'value')])
def update_output(value):
    return 'Threshold selected "{}"'.format(value)

#TARException rate Per Balance Slider
@app.callback(
dash.dependencies.Output('data-graph-tar-exception', 'figure'),
[dash.dependencies.Input('threshold-tar-exception-rate', 'value')])
def update_negative_rate_threshold(threshold):
    filtered_df = tarBalancesDF[tarBalancesDF.TARExceptionRate>threshold]
    filtered_balancesFigure =  px.scatter(filtered_df,x="Missions", y="TARExceptionRate", color="Balance")
    filtered_balancesFigure.update_layout(transition_duration=500)
    return filtered_balancesFigure

@app.callback(
dash.dependencies.Output('slider-output-tar-exception-rate', 'children'),
[dash.dependencies.Input('threshold-tar-exception-rate', 'value')])
def update_output(value):
    return 'Threshold selected "{}"'.format(value)



if __name__ == '__main__':
    app.run_server(debug=True)
