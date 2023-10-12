# dash_app.py
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button("Run Kedro Node", id="run-node-btn", n_clicks=0),
    html.Div(id="output-div")
])

@app.callback(
    Output("output-div", "children"),
    [Input("run-node-btn", "n_clicks")]
)
def run_kedro_node(n_clicks):
    if n_clicks > 0:
        # Logic to run Kedro node goes here
        pass

    return f"Button clicked {n_clicks} times."

if __name__ == "__main__":
