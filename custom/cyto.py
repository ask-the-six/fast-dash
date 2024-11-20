from dash import  html, dcc, Input, Output, callback
import dash_cytoscape as cyto
import dash_mantine_components as dmc

nodes = [
    {
        "data": {"id": short, "label": label},
        "position": {"x": 20 * lat, "y": -20 * long},
    }
    for short, label, long, lat in (
        ("la", "Los Angeles", 34.03, -118.25),
        ("nyc", "New York", 40.71, -74),
        ("to", "Toronto", 43.65, -79.38),
        ("mtl", "Montreal", 45.50, -73.57),
        ("van", "Vancouver", 49.28, -123.12),
        ("chi", "Chicago", 41.88, -87.63),
        ("bos", "Boston", 42.36, -71.06),
        ("hou", "Houston", 29.76, -95.37),
    )
]

edges = [
    {"data": {"source": source, "target": target}}
    for source, target in (
        ("van", "la"),
        ("la", "chi"),
        ("hou", "chi"),
        ("to", "mtl"),
        ("mtl", "bos"),
        ("nyc", "bos"),
        ("to", "hou"),
        ("to", "nyc"),
        ("la", "nyc"),
        ("nyc", "bos"),
    )
]
 
elements = nodes + edges


component = html.Div(
    [
        dcc.Dropdown(
            id="network-graphs-x-dropdown-update-layout",
            value="grid",
            clearable=False,
            options=[
                {"label": name.capitalize(), "value": name}
                for name in ["grid", "random", "circle", "cose", "concentric"]
            ],
        ),
        cyto.Cytoscape(
            id="network-graphs-x-cytoscape-update-layout",
            layout={"name": "grid"},
            style={"width": "100%", "height": "450px"},
            elements=elements,
        ),
        dmc.NavLink(
            label="Second parent link",
            childrenOffset=28,
            opened=True,
            children=[
                dmc.NavLink(label="First child link",children=[
                    dmc.NavLink(label="First child link"),
                    dmc.NavLink(label="Second child link"),
                    dmc.NavLink(label="Third child link"),
                ]),
                dmc.NavLink(label="Second child link"),
                dmc.NavLink(label="Third child link"),
            ],
        ),
    ]
)


@callback(
    Output("network-graphs-x-cytoscape-update-layout", "layout"),
    Input("network-graphs-x-dropdown-update-layout", "value"),
)
def update_layout(layout):
    return {"name": layout, "animate": True}
