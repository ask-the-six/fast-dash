from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

app = Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Hr(),  # Just to add a line for visual separation
    dash_table.DataTable(
        id='selected-data-table',
        columns=[
            {"name": i, "id": i} for i in df.columns
        ],
        data=[],
    ),
    dcc.Store(id='stored-selected-rows', data=[])  # Store for persisting selected row indices
])

@app.callback(
    Output('selected-data-table', "data"),  # Update the second data table
    Output('stored-selected-rows', 'data'),  # Update the stored data
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"),
    Input('stored-selected-rows', 'data')
)
def display_selected_data(rows, derived_virtual_selected_rows, stored_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    # Determine which rows have been newly selected or deselected
    new_selections = set(derived_virtual_selected_rows) - set(stored_selected_rows)
    deselections = set(stored_selected_rows) - set(derived_virtual_selected_rows)

    # Update the stored selected rows
    stored_selected_rows = list((set(stored_selected_rows) | new_selections) - deselections)

    dff = df if rows is None else pd.DataFrame(rows)

    # Extract the selected rows based on stored indices
    selected_data = df.iloc[stored_selected_rows]

    return selected_data.to_dict('records'), stored_selected_rows

if __name__ == '__main__':
    app.run_server(debug=True)
