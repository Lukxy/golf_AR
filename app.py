# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd

import plotly.graph_objs as go
# from dash.dependencies import Output, Input
from dash.dependencies import Input
from dash.dependencies import Output

#funktionen import
import math
# Instanz erstellen
app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Funktionen

# Reichweite berechnen
y_werte = []
x_werte = []
# for i in range(44):
#     y_werte.append( math.tan(math.pi/4) * i - 9.81 / (2 * 20**2.0 * (math.cos(math.pi/4))**2.0 ) * i**2.0 )
#     x_werte.append(i)

# Layout festlegen
fig = go.Figure(data=[go.Scatter(x= x_werte, y= y_werte )])

dcc.Graph(figure=fig)

app.layout = html.Div(children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    
    # benötigter Inputt
    # - GPS (Position) => Dropdown mit 5 verschiedenenen Positionen
    # - Loch-Auswahl (Position) => Dropdown der Löcher
    # - Windgeschwindigkeit (v in m/s) => random 
    # - Windrichtung (8 verschiedene Himmelsrichtungen in Grad rechnen lassen) => Random und aber Dropdown auswaählbar
    
    dcc.Dropdown(
        id='start-dropdown', 
        options=[
                {'label': 'Position 1', 'value': '0'},
                {'label': 'Position 2', 'value': '1'},
                {'label': 'Position 3', 'value': '2'},
                {'label': 'Position 4', 'value': '3'},
                {'label': 'Position 5', 'value': '4'}

        ],
        placeholder='Wähle eine Startposition',
        ),
        html.Div(id='dropdown'),

    dcc.Dropdown(
        id='ziel-dropdown',
        options=[
                {'label': 'Loch - Schlosshügel',    'value': '0'},
                {'label': 'Loch - Ententeich',      'value': '1'},
                {'label': 'Loch - Am Biergarten',   'value': '2'},
                {'label': 'Loch - Schafswiese',     'value': '3'},
                {'label': 'Loch - schöne Aussicht', 'value': '4'}

        ],
        placeholder='Wähle ein Ziel-Loch',
    ),

    html.Div(
        id = 'graf'
    ),

    # Ausgabe:
    # - Abfluggeschwindigkeit des Balls
    #   -> 4 verschiedene Kategorien für Abfluggeschwindigkeit
    # - Korrekturwinkel für Wind
    dcc.Graph(
        id='Flugbahn',
        figure=fig
    ),
    html.Div(id="textarea-1",children = [])
])

####################################
# CALLBACKS #######################
@app.callback(
    Output('graf', 'children'),
    # Output('Flugbahn', 'figure'),
    # Output('textarea-1', 'children'),
    [Input('start-dropdown', 'value'), Input('ziel-dropdown', 'value')],
    prevent_initial_call = True,
)
def update_graf(pos1, pos2):
    pos = []
    if pos1:
        pos.append("".join(pos1))
    if pos2:
        pos.append(''.join(pos2))
    # return print(pos)

    # # p1 = ''.join(map(str, pos1))#''.join(pos1)
    # # p2 = ''.join(map(str, pos2))#''.join(pos2)
    # p1 = [''.join(pos1)]
    # p2 = [''.join(pos2)]
    # p1 = int(float(pos1))
    # p2 = int(float(pos2))

    if pos1:
        if pos2:
            start_list = [[1, 230, 304], [2, 344, 99], [3, 122, 593], [4, 23, 215], [5, 412, 376]]
            ziel_list = [[1, 345, 212], [2, 356, 123], [3, 432, 348], [4, 3465, 234], [5, 500, 2123]]
            x = int(ziel_list[int(pos[1])][1]) - int(start_list[int(pos[0]) ][1])
            y = int(ziel_list[int(pos[1])][2]) - int(start_list[int(pos[0])][2])
            entfernung = int(math.sqrt( ((x**2) + (y**2)) ))
            print('Entfernung',entfernung)
            y_werte = []
            x_werte = []
            i= 0
            gamma = math.pi / 6
            v =math.sqrt( (entfernung * 9.81 / math.sin((2*gamma))) )
            print('Geschw.:', v )
            for i in range(entfernung):
                y_werte.append( math.tan(gamma) * i - 9.81 / (2 * v**2.0 * (math.cos(gamma))**2.0 ) * i**2.0 )
                x_werte.append(i)
            # print(y_werte)
            # print(x_werte)
            fig = go.Figure(data=[go.Scatter(x= x_werte, y= y_werte )])
            fig.update_yaxes(fixedrange=True)
            yr = [0, 50]
            xr = [0, 300] #maximale Schlag weite eines Profis sind ca. 300 meter
            fig.update_yaxes(range=yr)
            fig.update_xaxes(range=xr)
            # dcc.Graph(figure=fig)
            return html.Div(dcc.Graph(figure=fig))
    return print(pos)

if __name__ == '__main__':
    app.run_server(debug=True)
