import dash
from dash import dcc, html, Output, Input, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import yaml
from utils import config_ui as config
from dash import Dash
from utils.config_ui import create_appshell


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    update_title=None,
)

test = dash.page_registry.values()
# ... [Other initializations and functions]
app.layout = create_appshell(dash.page_registry.values())
server = app.server


if __name__ == "__main__":
   app.run_server(debug=True, port='6606')
