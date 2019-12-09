#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 23:45:53 2019

@author: wanyuzhong
"""
#Make sure to prepare your environment:
#pip install dash==0.28.5 # The core dash backend
#pip install dash-html-components==0.13.2 # HTML components
#pip install dash-core-components==0.35.0 # Supercharged components
#pip install dash-bootstrap-components

# Import the necessary packages
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd


app = dash.Dash(__name__)

#Read excel file into a data frame
df =  pd.read_excel('https://s3.amazonaws.com/programmingforanalytics/NBA_data.xlsx')
col = df.columns
var = list(col) 
var.pop(0) #Remove 'Name'
var.pop(0) #Remove 'Team'
var.pop(-2) #Remove 'Plus_minus'


navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Group Member",
            children=[
                dbc.DropdownMenuItem("Jennifer Nguyen"),
                dbc.DropdownMenuItem("Mengxin Tan"),
                dbc.DropdownMenuItem("Colin Wood"),
                dbc.DropdownMenuItem("Wendy Zhong")
            ],
        ),
    ],
    brand="NBA Players: Age, Game Stats and Salary",
    brand_href="#",
    sticky="top",
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("About our app"),
                        html.P(
                            """\
This Dash application contains information about names, teams, salaries, and game statistics of 20 famous basketball players in this new season. We saw that the salaries were very unevenly distributed among players. Hence, we decided to look at how players’ performances and salaries are related to each other.
We display all information in a table so that users can easily look up information and compare characteristics among players. In addition, we made a scatter plot to show the correlation between performances and salaries. By default setting, we will get a positive relationship between age and salary. Users are also free to choose what variables for which axes they want to browse. 
We believe that there will be a clearer trend if a larger data sample is provided.
"""
                        )
                    ],
                    md=4,
                ),
                            
                dbc.Col(
                    [
                        html.H2("Graph"),
                        dcc.Graph(id = 'NBA',
                                      figure = {
                                              'data': [
                                                      {'x':df['Name'], 'y':df['Salary'], 'type': 'bar', 'name':'dollar'},
         
                          ],
                                              'layout':{'title': "Players' Salary Distribution"}
                          })
                                      
                   
                   ]   
                ),
            ]
        ),
        dbc.Row( 
                [
                dbc.Col([
                html.H2("Player's Information"),
                html.P("The table can be sorted by each column:"),
                dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
                fixed_rows={ 'headers': True, 'data': 0 },
                style_cell={'width': '100px'},
                style_data_conditional=[
                    {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                
                sort_action='native',
                sort_mode='single'
               )]
                )]
                
                ),
                
        dbc.Row(html.H2("Correlation between variables"),
                ),
                
        dbc.Row([
                dbc.Col([
                html.H5("Choose a variable for x-axis"),
                html.Div([
                        dcc.Dropdown(
                        id='xaxis-column',
                        options=[{'label': i, 'value': i} for i in var],
                        value='Age'
                        )],
                style={'width': '48%', 'display': 'inline-block'})
                        ]),
                        
                dbc.Col([
                html.H5("Choose a variable for y-axis"),
                html.Div([
                        dcc.Dropdown(
                        id='yaxis-column',
                        options=[{'label': i, 'value': i} for i in var],
                        value='Salary'
                        )],
                style={'width': '48%', 'display': 'inline-block'})
                ])
                        ]),
                        
        dbc.Row(dcc.Graph(id='scatter-plot'))


    ],
    className="mt-4",
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([navbar, body])

@app.callback(
     Output('scatter-plot', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')])


def update_graph(xaxis_column_name, yaxis_column_name):

    return {
        'data': [dict(
            x=df[xaxis_column_name],
            y=df[yaxis_column_name],
            text = df['Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'},
                }
        )],
    
        'layout': dict(
            xaxis={
                'title': xaxis_column_name
            },
            yaxis={
                'title': yaxis_column_name
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == "__main__":
    app.run_server()
