import os
import dash_mantine_components as dmc
from dash import Output, Input, html, callback
import pandas as pd

def create_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table

csv_files = [f for f in os.listdir('src/dis/CDB90/src-data/M000121') if f.endswith('.csv')]

#  For each csv file we use the dmc accordion component to display the data in a collapsible format and display the contents as dataframes

def create_accordion(file):
    df = pd.read_csv(f'src/dis/CDB90/src-data/M000121/{file}',comment='=')
    return   dmc.Table(
                id=f"table-{id}",
                data=df.to_dict(),
            )
disp=[]
for file in csv_files:
    disp.append({"value": create_accordion(file), "label": file})


#  We use the dmc accordion component to display the data in a collapsible format and display the contents as dataframes
component = html.Div(
    [
        dmc.SegmentedControl(
            id="segmented",
            value="ng",
            data=disp,
            mb=10,
        ),
        dmc.Text(id="segmented-value"),
    ]
)