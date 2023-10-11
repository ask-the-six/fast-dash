from dash import html, dash_table, html
import dash_mantine_components as dmc


def create_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table


def create_accordion_label(name, website, description):
    return dmc.AccordionControl(
        dmc.Group(
            [
                dmc.Avatar(src=f"{website}favicon.ico", radius="xl", size="lg"),
                html.Div(
                    [
                        dmc.Text(name),
                        dmc.Text(description, size="sm", weight=400, color="dimmed"),
                    ]
                ),
            ]
        )
    )



def create_interactive_table_layout(df):
    """
    Create an interactive table layout for Dash using the provided dataframe.

    Parameters:
    - df (pd.DataFrame): The dataframe to display in the table.

    Returns:
    - html.Div: The Dash layout containing the interactive table.
    """
    return html.Div([
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
        html.Div(id='datatable-interactivity-container')
    ])