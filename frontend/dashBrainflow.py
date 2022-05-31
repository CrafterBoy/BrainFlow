import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np
from datetime import datetime,timedelta, date
from dash import State
# from functions_plot import get_table_info, get_web_data, read_log_error
from sqlalchemy import create_engine
import time

df = None

def generate_rows_errors(row):
    return html.P(row)


dropdownUser = dbc.DropdownMenu(
    label="Users",
    children=[
        dbc.DropdownMenuItem("MJ"),
        dbc.DropdownMenuItem("Jaume"),
        dbc.DropdownMenuItem("Salva"),
        dbc.DropdownMenuItem("Jordi"),
    ],
)

dropdownAcciones = dbc.DropdownMenu(
    label="Acciones",
    children=[
        dbc.DropdownMenuItem("Andar"),
        dbc.DropdownMenuItem("Escuchar musica"),
        dbc.DropdownMenuItem("Hablar"),
    ],
    style={'width': '49%', 'display': 'inline-block'}
)

tab1_content = dbc.Card(
    dbc.CardBody(
        [
                dbc.Container([
                    html.Div(
                        dbc.Row(
                                [
                                    dbc.Col(html.P("Usuarios: "), width=1),
                                    dbc.Col(dropdownUser, width=2),
                                    dbc.Col(html.P("Lote: 5985985"), width=3),
                                    dbc.Col(html.P("Accion"), width=1),
                                    dbc.Col(dropdownAcciones, width=3),
                                ],
                        ),
                        style={'margin-bottom' : '50px'}  
                    ),
                html.Div([dbc.Button("Play", color="primary", className="me-1"),
                        dbc.Button("Save", color="success", className="me-1"),
                        dbc.Button("Cancel", color="danger", className="me-1")],        
                ),
                html.Div(
                    children=[
                        html.H1("Grafico con todos los sensores que guardaremos")
                    ],
                    style={"marginTop": "1%", "marginBottom": "1%"}
                ),
                dcc.Graph(id="line-chart")
            ]
            ),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Container([
                html.Div(
                    children=[
                        html.H1("Todos los sensores")
                    ],
                    style={"marginTop": "1%", "marginBottom": "1%"}
                ),
                dcc.Graph(id="line-chart2")
            ]
            ),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
    ]
)


navbar = dbc.Navbar(
    [
        dbc.NavbarBrand("Open BCI Interface", className="ms-2"),
        dbc.Col()
    
    ],
    color="dark",
    dark=True
)

# Initialize the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

offcanvas = html.Div(
    [
        dbc.Button("Registrar usuarios/acciones", id="open-offcanvas", n_clicks=0, className="position-absolute top-5 end-0 mx-3"),
        dbc.Offcanvas(
            dbc.Row([

                # dbc.Col(children=[generate_rows_errors(i) for i in read_log_error()])

            ]),
            id="offcanvas",
            title="Error logs",
            is_open=False,
            placement="end",
            style={"width" : '45%'}
        ),
    ]
)



app.layout = html.Div(children=[
    navbar,
    offcanvas,
    tabs,
    
   
])


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)

