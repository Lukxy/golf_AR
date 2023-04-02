# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

#########################################################################################################################################################################################
# beim ersten starten tritt ein Fehler auf:                                                                                                                                             #
#  ImportError: cannot import name 'get_current_traceback' from 'werkzeug.debug.tbtools' (C:\Users\...\anaconda3\envs\Projekt_AR_Golf\lib\site-packages\werkzeug\debug\tbtools.py)      #
#                                                                                                                                                                                       #
# Dieser lässt sich einfach beheben:                                                                                                                                                    #   
#  -> in Datei \dash.py navigieren                                                                                                                                                      #   
#  -> in Datei \dash.py navigieren                                                                                                                                                      #   
#       ->            C:\Users\NAME\anaconda3\envs\Projekt_AR_Golf\Lib\site-packages\dash\dash.py                                                                                       #   
#  -> Zeile 22: from werkzeug.debug.tbtools import get_current_traceback                                                                                                                #
#  -> ändern zu: from werkzeug.debug.tbtools import DebugTraceback                                                                                                                      #   
#  -> get_current_traceback   wird zu   DebugTraceback                                                                                                                                  #   
#                                                                                                                                                                                       #
# https://github.com/plotly/dash/issues/1992                                                                                                                                            #
#########################################################################################################################################################################################

#############
# Wir verwenden das Framework dash / plotly
#############

#import von anderen Files
import flugbahn_berechnung as flugbahn

from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
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

# Werte für die Berechnung
y_werte = []
x_werte = []

# Festlegen vom Layout der Seite
app.layout = html.Div(children=[
    # Überschrift der Seite
    html.H1(
        children='Golf-AR',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    # einfacher Text:
    html.Div(children='Damit du den perfekten Schlag machst!', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div(children='Das Dieagramm geht bis 300m, diese Weite entspricht eineSchalgweite eines Profispielers.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    # Auswahl von der Startposition
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
    # Auswahl der Lochposition
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
])

####################################
# CALLBACKS #######################
@app.callback(
    Output('graf', 'children'),
    [Input('start-dropdown', 'value'), Input('ziel-dropdown', 'value')],
    prevent_initial_call = True,
)
def update_graf(pos1, pos2):
    pos = []
    if pos1:
        pos.append("".join(pos1))
    if pos2:
        pos.append(''.join(pos2))

    if pos1:
        if pos2:
            #Steigwinkel wird als konstant angenommen
            # Berechnung:
            gamma = math.pi / 6

            ablenkwinkel = flugbahn.ablenkwinkel(pos, gamma)

            werte = flugbahn.berechne(pos, gamma)
            
            # Updaten der des Diagramms
            fig = px.line_3d(werte, x="x", y="z", z="y", range_x=[0, 300], range_y=[0, 2], range_z = [0, 50])
           
            #Ansicht ändern
            fig.update_layout(scene_camera=dict( eye=dict( x=-2, y=-0.6, z=0.1 ) ) )
            
            return dcc.Graph(figure=fig, style={'width': '90vh', 'height': '90vh'})
    return pos

if __name__ == '__main__':
    app.run_server(debug=True)
