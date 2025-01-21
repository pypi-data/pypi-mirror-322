import os
import webbrowser
import pandas as pd
from dash import Dash, Input, Output, dash_table, dcc, html

from modules.fimport import path_output

# File options
file_options = [
    'Surgery-Default.log',
    'Surgery-Debug.log',
    'Surgery-Software-reserved.log',
    'Surgery-Installer.log'
]

def load_file(file_name):
    try:
        file_to_parse = os.path.join(path_output, file_name)
        with open(file_to_parse, 'r', encoding='latin1') as file:
            lines = file.readlines()
        data = []
        for line in lines:
            parts = line.split('\t')
            if len(parts) >= 6:
                timestamp, level, source, id_info, code, message = parts[:6]
                date, time = timestamp.split('T') if 'T' in timestamp else (timestamp, '')
                time = time.split('.')[0] if '.' in time else time
                data.append({
                    'Date': date,
                    'Time': time,
                    'Level': level,
                    'Source': source,
                    'ID Info': id_info,
                    'Code': code.strip(),
                    'Message': message.strip()
                })

        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Unable to read file: {e}")
        return pd.DataFrame()

# Initial load
initial_file = file_options[0]
df = load_file(initial_file)

# Create app Dash
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Elite Log Viewer"

# Layout
app.layout = html.Div([
    html.H1("Elite Log Viewer"),
    
    html.Div([
        html.Label("Select File:"),
        dcc.Dropdown(
            id='file-selector',
            options=[{'label': file, 'value': file} for file in file_options],
            value=initial_file,
            style={'width': 300, 'margin-bottom': '20px'}
        )
    ]),

    html.Div([
        dcc.DatePickerSingle(
            id='filter-date',
            placeholder='date',
            display_format='YYYY-MM-DD',
            style={
                'width': 200,
                'height': 30,
                'border-color': '#DFE6E9',
                'textAlign': 'left',
                'font-size': '10px',
                'verticalAlign': 'middle',
            },
        ),
        html.Div([
            html.Label("Level filter"),
            dcc.Checklist(
                id='filter-level',
                options=[],
                value=[],
                inline=False,
            ),
        ]),
        dcc.Dropdown(
            id='filter-source',
            options=[],
            placeholder='Filtro Source',
            style={
                'width': 200,
                'height': 25,
                'border-color': '#DFE6E9',
                'textAlign': 'left',
                'font-size': '12px',
                'verticalAlign': 'middle',
                'margin-top': 10,
            },
        ),
        dcc.Dropdown(
            id='filter-code',
            options=[],
            placeholder='Code filter',
            style={
                'width': 200,
                'height': 30,
                'border-color': '#DFE6E9',
                'textAlign': 'left',
                'font-size': '12px',
                'verticalAlign': 'middle',
                'margin-top': 10,
            },
        ),
        dcc.Input(
            id='search-message',
            type='text',
            placeholder='Message filter',
            style={
                'width': 200,
                'height': 30,
                'border-color': '#DFE6E9',
                'textAlign': 'left',
                'font-size': '14px',
                'verticalAlign': 'middle',
                'margin-top': 10,
            },
        ),
    ], style={'margin-bottom': '20px'}),

    dash_table.DataTable(
        id='log-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        page_size=50,
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '5px',
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{Level} = "emerg"'},
                'backgroundColor': 'red',
                'color': 'white',  # white text
            },
            {
                'if': {'filter_query': '{Level} = "alert"'},
                'backgroundColor': 'pink',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{Level} = "crit"'},
                'backgroundColor': 'lightblue',
                'color': 'black',
            }
        ]
    )
])

# Callback for file selection
@app.callback(
    [Output('filter-level', 'options'),
     Output('filter-source', 'options'),
     Output('filter-code', 'options')],
    Input('file-selector', 'value')
)
def update_filter_options(selected_file):
    new_df = load_file(selected_file)
    if not new_df.empty:
        level_options = [{'label': lvl, 'value': lvl} 
                         for lvl in sorted(new_df['Level'].dropna().unique())
                         ]
        source_options = [{'label': src, 'value': src} 
                          for src in sorted(new_df['Source'].dropna().unique())
                          ]
        code_options = [{'label': code, 'value': code} 
                        for code in sorted(new_df['Code'].dropna().unique())
                        ]
    else:
        level_options = source_options = code_options = []
    return level_options, source_options, code_options

# Callback for update data table
@app.callback(
    Output('log-table', 'data'),
    [
        Input('filter-date', 'date'),
        Input('filter-level', 'value'),
        Input('filter-source', 'value'),
        Input('filter-code', 'value'),
        Input('search-message', 'value'),
        Input('file-selector', 'value')
    ]
)
def filter_data(filter_date, filter_levels, filter_source, filter_code, search_message, selected_file):
    filtered_df = load_file(selected_file)

    if not filtered_df.empty:
        if filter_date:
            filtered_df = filtered_df[filtered_df['Date'] == filter_date]
        if filter_levels:
            filtered_df = filtered_df[filtered_df['Level'].isin(filter_levels)]
        if filter_source:
            filtered_df = filtered_df[filtered_df['Source'] == filter_source]
        if filter_code:
            filtered_df = filtered_df[filtered_df['Code'] == filter_code]
        if search_message:
            filtered_df = filtered_df[filtered_df['Message'].str.contains(search_message, case=False, na=False)]

    return filtered_df.to_dict('records')


if __name__ == "__main__":
    url = "http://127.0.0.1:8050"
    webbrowser.open_new(url)
    app.run_server(debug=False)

