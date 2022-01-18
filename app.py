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
balDF = pd.read_csv('balance_all_val.csv', sep=',')
print("Data read.")

tableDF = balDF

# new figure
balancesFigure = px.scatter(balancesDF,x="NumMissions", y="AvgWeightDiff", color="Balances")
negWeightBalances = px.scatter(negWeightDF,x="Missions", y="NegativeWeightRate", color="Balance")
tarExceptionBalances = px.scatter(tarBalancesDF,x="Missions", y="TARExceptionRate", color="Balance")

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Balea Data Analysis'),

    dcc.Tabs([
        dcc.Tab(label='Différence entre poids théorique et mesuré', children=[
            dcc.Graph(
        id='data-graph-balance-weight-diff',
        figure=balancesFigure
    ),
                dcc.Slider(
        id='threshold-difference-weight',
        min=0,
        max=1.1,
        step=0.01,
        value=0.4
    ),
    html.Div(id='slider-output-difference-weight')
        ]),
        
        dcc.Tab(label='Analyse ratio négatif par Balance', children=[
            dcc.Graph(
        id='data-graph-negative-rate',
        figure=negWeightBalances
    ),
    dcc.Slider(
        id='threshold-negative-rate',
        min=0,
        max=0.10,
        step=0.01,
        value=0.03

    ),
    html.Div(id='slider-output-container')
        ]),
        dcc.Tab(label='Analyse TAR Exception par Balance', children=[
            dcc.Graph(
        id='data-graph-tar-exception',
        figure=tarExceptionBalances
    ),

    dcc.Slider(
        id='threshold-tar-exception-rate',
        min=0,
        max=0.15,
        step=0.01,
        value=0.05

    ),
    html.Div(id='slider-output-tar-exception-rate')
        ]),
    
    dcc.Tab(label='Balances classés défectueuses', children=[
        html.Div(id='slider-output-container-neg'),
        html.Div(id='slider-output-container-tar'),
        html.Div(id='slider-output-container-wgt'),
        dash_table.DataTable(
                    id = 'data-list-bad-balances',
                    columns = [{"name":i, "id":i} for i in sorted(tableDF.columns)],
                    data = tableDF.to_dict('records'),
                    page_size=25
                    )
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

@app.callback(
dash.dependencies.Output('slider-output-container-neg', 'children'),
[dash.dependencies.Input('threshold-negative-rate', 'value')])
def update_output(value):
    return 'Ratio seuil pour valeurs négatives : {}'.format(value)

@app.callback(
dash.dependencies.Output('slider-output-container-tar', 'children'),
[dash.dependencies.Input('threshold-tar-exception-rate', 'value')])
def update_output(value):
    return 'Ratio seuil pour TAR Exceptions : {}'.format(value)

@app.callback(
dash.dependencies.Output('slider-output-container-wgt', 'children'),
[dash.dependencies.Input('threshold-difference-weight', 'value')])
def update_output(value):
    return 'Valeur seuil pour poids : {}'.format(value)

@app.callback(
dash.dependencies.Output('data-list-bad-balances', 'data'),
dash.dependencies.Input('threshold-tar-exception-rate', 'value'),
dash.dependencies.Input('threshold-difference-weight', 'value'),
dash.dependencies.Input('threshold-negative-rate', 'value'))
def update_selected_balances(t1, t2, t3):
    filtered_df = balDF[balDF.ExceptionRate>t1]
    filtered_df = filtered_df[filtered_df.WeightDiff>t2]
    tableDF = filtered_df[filtered_df.NegRate>t3]
    return tableDF.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
