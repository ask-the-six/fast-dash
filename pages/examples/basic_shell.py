import dash_mantine_components as dmc
import dash.dependencies as dd
from dash import Dash, html, register_page, callback
from dash.dependencies import Input, Output

register_page(__name__, icon="fa:bar-chart", section='Examples', href='/shell')

# Navbar is initially hidden
navbar = dmc.Navbar(
    id="navbar",
    p="md",
    hidden=False,
    width={"sm": 200, "lg": 300},
    children="Application navbar",
)

aside = dmc.MediaQuery(
    smallerThan="sm",
    styles={"display": "none"},
    children=dmc.Aside(p="md", hiddenBreakpoint="lg", children="Application sidebar", width={"sm": 200, "lg": 300}),
)

footer = dmc.Footer(height=60, p="md", children="Application footer")

header = dmc.Header(
    height=70,
    p="md",
    children=html.Div(
        style={"display": "flex", "alignItems": "center", "height": "100%"},
        children=[
            # Directly place the burger without the MediaQuery wrapper
            dmc.Burger(id="burger", opened=False, size="sm", color="gray", mr="xl"),
            "Application header",
        ],
    ),
)

color_scheme = "dark"

appshell = dmc.AppShell(
    styles={
        "main": {
            "background": "#1A1B1E" if color_scheme == "dark" else "#f8f9fa",
        },
    },
    navbarOffsetBreakpoint="sm",
    asideOffsetBreakpoint="sm",
    aside=aside,
    footer=footer,
    header=header,
    children=[
        html.P("Resize app to see responsive navbar in action"),
    ],
)

layout = dmc.MantineProvider(
    withNormalizeCSS=True, withGlobalStyles=True, theme={"colorScheme": color_scheme}, children=appshell
)

@callback(dd.Output("navbar", "width"), dd.Input("burger", "opened"))
def adjust_navbar_width(opened):
    if opened:
        return {"sm": 300, "lg": 400, "base": 300}  # Adjusted values
    else:
        return {"sm": 30, "lg": 75, "base": 75}  # Adjusted values

