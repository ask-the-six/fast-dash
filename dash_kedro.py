from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path

# Define your alternative parameters
alt_params = {
    "param1": "value1_alt",
    "param2": "value2_alt",
    # ... add more parameters as needed
}

# Path to your Kedro project root
project_path = Path("<project_root>")

# Bootstrapping the Kedro project
bootstrap_project(project_path)

# Create a Kedro session with the alternative parameters
with KedroSession.create("<package_name>", project_path=project_path, extra_params=alt_params) as session:
    # Run the specific pipeline
    session.run(pipeline_name="my_pipeline")








# kedro_pipeline.py
from kedro.pipeline import node, Pipeline

def example_node(firstname, lastname):
    print(f"Hello, {firstname} {lastname}!")

example_pipeline = Pipeline([node(func=example_node, inputs=["firstname", "lastname"], outputs=None, name="example_node")])
###
# dash_app.py
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='firstname-input', type='text', placeholder='First Name'),
    dcc.Input(id='lastname-input', type='text', placeholder='Last Name'),
    html.Button('Submit', id='submit-button'),
    html.Div(id='output-div')
])

@app.callback(
    Output("output-div", "children"),
    [Input("submit-button", "n_clicks")],
    [dash.dependencies.State('firstname-input', 'value'),
     dash.dependencies.State('lastname-input', 'value')]
)
def run_kedro_node(n_clicks, firstname, lastname):
    if n_clicks and firstname and lastname:
        # Logic to run Kedro node with firstname and lastname parameters goes here
        pass

    return "Pipeline executed."

if __name__ == "__main__":
    app.run_server(debug=True)



####


# ... (rest of the code from dash_app.py)

from kedro.context import load_context
from kedro.pipeline import node, Pipeline
from kedro.runner import SequentialRunner

# Load the Kedro project context
project_path = "."  # adjust as necessary
context = load_context(project_path)

# Assuming you've defined your pipeline in kedro_pipeline.py
from kedro_pipeline import example_pipeline

@app.callback(
    Output("output-div", "children"),
    [Input("submit-button", "n_clicks")],
    [dash.dependencies.State('firstname-input', 'value'),
     dash.dependencies.State('lastname-input', 'value')]
)
def run_kedro_node(n_clicks, firstname, lastname):
    if n_clicks and firstname and lastname:
        # Manually set the parameters for the Kedro pipeline
        context.catalog.save("firstname", firstname)
        context.catalog.save("lastname", lastname)

        # Run the Kedro pipeline
        runner = SequentialRunner()
        runner.run(example_pipeline, context.catalog)

        return f"Hello, {firstname} {lastname}!"
    return "Enter names and click submit."

# ... (rest of the code from dash_app.py)
