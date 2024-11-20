import streamlit as st
import pandas as pd
from models.lanchester import LanchesterModel  # Ensure lanchester.py is in the same directory or install as a module

st.set_page_config(layout="wide")
st.header(":material/function: Lanchester Model Simulation",divider=True)

class PageText:

    intro = """

    In 1916, Frederick Lanchester published differential equations to model the attrition rates of soldiers in battle. They are known as the **Lanchester Square Law** of attrition and the **Linear Law** (Syms, 2017). Similar equations were published independently by M. Osipov in a Russian military journal at the same time (Helmbold, 1993).

    Lanchester’s Linear Model is based on the assumptions of ancient combat, where formations of soldiers using melee weapons attack one unit at a time within the reach of their weapon.

    where \( x \) and \( y \) represent the units for each opposing force at the beginning of a battle, and \( D \) and \( A \) are the rates at which each unit can destroy units from the opposing force within one unit of time \( t \) (Syms, 2017).
    """
    lin_law = r"""

    $$
    \frac{dx}{dt} = -D \cdot y \cdot x,
    $$

    $$
    \frac{dy}{dt} = -A \cdot x \cdot y,
    $$

    


    """

    sq_law = r"""

    $$
    \frac{dx}{dt} = -D \cdot y,
    $$

    $$
    \frac{dy}{dt} = -A \cdot x,
    $$

    """
    

def get_sim_results(model:LanchesterModel):
    model.run_simulation()
    results_df = model.get_results()

    tab1, tab2, tab3 = st.tabs(["Visualization", "Summary","Results Table"])

    # Results Table
    with tab1:
        st.header("Force Levels Over Time")
        st.line_chart(results_df.set_index("Step")[["Force X", "Force Y"]])

    # Summary
    with tab2:
        st.header("Summary")
        summary = model.get_summary()
        st.json(summary)

    # Visualization
    with tab3:
        st.header("Simulation Results")
        st.dataframe(results_df)

def sim_params():
    expander = st.expander("Sim Config", icon=":material/settings:")
    sp = {}
    with expander:
        sp['stopping_condition'] = st.selectbox("Stopping Condition", ["defeat", "attrition"], key="stopping_condition")
        if sp['stopping_condition'] == "attrition":
            sp['attrition_threshold'] = st.slider("Attrition Threshold (%)", min_value=0.0,max_value=99.9,value=30.0, key="attrition_threshold")
        sp['time_step'] = st.number_input("Time Step", value=0.1, key="time_step")
        sp['max_steps'] = st.number_input("Max Steps", min_value=1, value=1000, key="max_steps")
    return sp
    




col1, col2 = st.columns([1, 4])
model = LanchesterModel()
options = ["linear", "square"]




with col1:
    selection = st.segmented_control('Model',options, selection_mode="single")
    if selection == "square":
        st.markdown(PageText.sq_law)
    elif selection == "linear":
        st.markdown(PageText.lin_law)
    sp = sim_params()
    x_force = st.expander('### X Forces', expanded=True,icon=':material/swords:')
    y_force = st.expander('### Y Forces', expanded=True,icon=':material/swords:')


model.y0 = y_force.slider("Initial Units for Force Y", value=150,max_value=100000, key="y0")
model.D = y_force.number_input("Attrition Rate (D) for Force Y's Effect on Force X", value=0.02, key="D")
model.x0 = x_force.slider("Initial Units for Force X", value=100,max_value=100000, key="x0",step=10)
model.A = x_force.number_input("Attrition Rate (A) for Force X's Effect on Force Y", value=0.01, key="A")
model.model = selection
model.time_step = sp['time_step']
model.max_steps = sp['max_steps']
model.stopping_condition = sp['stopping_condition']
try:
    model.attrition_threshold = sp['attrition_threshold']
except KeyError:
    pass

    

with col2:
    st.markdown(PageText.intro)
    get_sim_results(model)

