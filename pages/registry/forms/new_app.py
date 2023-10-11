from dash import html
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
from dash import Input, Output, html, callback
import json

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



