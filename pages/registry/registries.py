from dash import dcc, html, Input, Output, callback, register_page
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
from dash.dependencies import Input, Output
import json
from utils import utils as u
register_page(__name__, icon="ph:squares-four-duotone",section='registry')

df = df = pd.read_parquet('app_metadata.parquet')
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
                dmc.Avatar(src=u.get_favicon_url(website), radius="xl", size="lg"),
                html.Div(
                    [
                        dmc.Text(name),
                        dmc.Text(description, size="sm", weight=400, color="dimmed"),
                    ]
                ),
            ]
        )
    )

fields = [
    "id", "name", "description", "tags", "repository_url", "website", "image_url", 
    "doc_url", "added_by", "added_by_name", "created_at", "updated_at", "version_id",
    "version_code", "version", "install_script", "start_script", "app_port", "ui_path",
    "remarks", "version_created_at", "version_updated_at", "version_added_by"
]

output_fields = [Output(f"{field}-input", "value") for field in fields]









def create_app_card_content(app_data):
    cardcontent=  [
        dmc.CardSection(
            children=[
                dmc.Group(
                    children=[
                        dmc.Text(f"Default Version: {app_data['name']}=={app_data['version']}", weight=500),
                        dmc.Menu([
                            dmc.MenuTarget(dmc.ActionIcon(DashIconify(icon="carbon:overflow-menu-horizontal"), color="gray", variant="transparent")),
                            dmc.MenuDropdown([
                                dmc.MenuItem("Versions", id=f"versions-{app_data['id']}"),
                                dmc.MenuItem("Show Details", id=f"details-{app_data['id']}"),
                                dmc.MenuItem("New Version", id=f"new-version-{app_data['id']}")
                            ])
                        ])
                    ],
                    position="apart",
                )
            ],
            withBorder=True,
            inheritPadding=True,
            py="xs",
        ),
       
        dmc.CardSection(
            children=[
                dmc.Text(
                    app_data['website'],
                    mt="sm",
                    color="blue",
                ),
                dmc.Text(
                    children=app_data['added_by_name'],
                    mt="sm",
                    color="dimmed",
                    size="sm",
                )
            ]
        ),
        dmc.CardSection(
            children=[
                dmc.SimpleGrid(
                    cols=2, 
                    children=[
                        dmc.Text("Version:", color="dimmed"),
                        dmc.Text("Tags:", color="dimmed"),
                        dmc.Group(
                            children=[dmc.Badge(tag) for tag in app_data['tags']], 
                            position="center"
                        )
                    ],
                )
            ],
            inheritPadding=True,
            mt="sm",
            pb="md",
        ),
    ]
    return cardcontent

def create_app_card(app_data):
    return dmc.AccordionItem(
        [
            create_accordion_label(app_data['name'], app_data['website'], app_data['description']),
            dmc.AccordionPanel(dmc.Card(
                children=create_app_card_content(app_data),
                withBorder=True,
                shadow="sm",
                radius="md",
                style={"width": 300}
            ))
        ],
        value=app_data['id']
    )

# Create list of cards from dataframe
cards = [create_app_card(row) for _, row in df.iterrows()]

local_apps_ui = html.Div([
    dmc.Accordion(
        chevronPosition="right",
        variant="contained",
        children=cards
    )
])
modal = dmc.Modal(
    title="Edit Version",
    id="version-modal",
    size="lg",
    centered=True,
    zIndex=10000,
    children=[
        dmc.SimpleGrid(
    cols=2,
    children=[
         dmc.SimpleGrid(
            cols=1,
            children=[
                dmc.Text("Current Version", size="xl"),
                html.Div(id="current-version-details", children=[]),
            ]),
            dmc.SimpleGrid(
            cols=1,
            children=[
                dmc.TextInput(id="id-input", label="ID"),
                dmc.TextInput(id="name-input", label="Name"),
                dmc.Textarea(id="description-input", label="Description"),
                dmc.MultiSelect(id="tags-input", data=[], label="Tags", searchable=True, style={"width": 400}),
                dmc.TextInput(id="repository-url-input", label="Repository URL"),
                dmc.TextInput(id="website-input", label="Website"),
                dmc.TextInput(id="image-url-input", label="Image URL"),
                dmc.TextInput(id="doc-url-input", label="Doc URL"),
                dmc.TextInput(id="added-by-input", label="Added By"),
                dmc.TextInput(id="added-by-name-input", label="Added By Name"),
                dmc.TextInput(id="version-id-input", label="Version ID"),
                dmc.TextInput(id="version-code-input", label="Version Code"),
                dmc.TextInput(id="version-input", label="Version"),
                dmc.Textarea(id="install-script-input", label="Install Script"),
                dmc.Textarea(id="start-script-input", label="Start Script"),
                dmc.TextInput(id="app-port-input", label="App Port"),
                dmc.TextInput(id="ui-path-input", label="UI Path"),
                dmc.Textarea(id="remarks-input", label="Remarks"),
                dmc.Button("Save", id="save-button", mt="md")

            ])
        ])
    ]
)



layout = html.Div([
    dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.Tab("Local", value="local"),
                    dmc.Tab("Remote-Private", value="remote-private"),
                    dmc.Tab("Public", value="public"),
                ]
            ),
            dmc.TabsPanel(value="local", children=[local_apps_ui]),
            dmc.TabsPanel(value="remote-private", children=["This is the content for the Remote-Private tab."]),
            dmc.TabsPanel(value="public", children=["This is the content for the Public tab."]),
        ],
        orientation="vertical",
        value="local",
    ),
    html.Div(id='currently-editing', style={'display': 'none'}),
    html.Div(id="output-version"),
    html.Div(id="output-details"),
    html.Div(id="output-new-version"),
    html.Div(id="intermediate-value", style={"display": "none"}),
    modal
    
])

@callback(
    Output("output-version", "children"),
    [Input(f"versions-{row['id']}", "n_clicks") for _, row in df.iterrows()]
)
def show_versions(*args):
    # Add logic to show versions or any other desired behavior
    return "Showing versions..."

@callback(
    Output("output-details", "children"),
    [Input(f"details-{row['id']}", "n_clicks") for _, row in df.iterrows()]
)
def show_details(*args):
    # Add logic to show details or any other desired behavior
    return "Showing details..."

@callback(
    Output("output-new-version", "children"),
    [Input(f"new-version-{row['id']}", "n_clicks") for _, row in df.iterrows()]
)
def add_new_version(*args):
    # Add logic to add new version or any other desired behavior
    return 

@callback(
    [Output("version-modal", "opened"), Output('currently-editing', 'children')],
    [Input(f"new-version-{row['id']}", "n_clicks") for _, row in df.iterrows()],
    prevent_initial_call=True,
)
def open_edit_version_modal(*args):
    for idx, click in enumerate(args):
        if click:
            return True, df.iloc[idx]['id']
    return False, dash.no_update


@callback(
    [Output("intermediate-value", "children"),
     Output("current-version-details", "children")],
    [Input(f"new-version-{row['id']}", "n_clicks") for _, row in df.iterrows()],
    prevent_initial_call=True,
)
def populate_form(*args):
    for idx, click in enumerate(args):
        if click:
            current_id = df.iloc[idx]["id"]
            selected_data = df[df['id'] == current_id].iloc[0].to_dict()
            
            # Create a list of current version details to display
            current_version_display = []
            for key, value in selected_data.items():
                current_version_display.append(html.Div(f"{key}: {value}"))
            
            return json.dumps(selected_data), current_version_display
    raise dash.exceptions.PreventUpdate




