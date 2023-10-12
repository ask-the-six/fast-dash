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
    [Input("run-node-btn", "n_clicks")]
)
def run_kedro_node(n_clicks):
    if n_clicks > 0:
        # Run the Kedro node
        runner = SequentialRunner()
        runner.run(example_pipeline, context.catalog)

        return "Kedro node executed!"
    return f"Button clicked {n_clicks} times."

# ... (rest of the code from dash_app.py)
