from dash import dcc, register_page
import dash_mantine_components as dmc

register_page(__name__, path="/", icon="akar-icons:info",section='Home')

layout = dmc.Container(
    [
        dmc.Title("Welcome to the home page"),
        dcc.Markdown(
    """
    ### Multi-page App Demo

    This demonstration showcases a multi-page app structured with nested folders inside the `pages` directory:

    ```
    - app.py 
    - pages
        - chapter1                  
           |-- page1.py
           |-- page2.py
        - chapter2                   
           |-- page1.py
           |-- page2.py    
        - home.py        
    ```

    ### Enhancing Page Registry

    The app provides a feature to augment the `page_registry` with custom data. Here, we're adding icons:

    ```python
    dash.register_page(__name__, icon="fa:bar-chart")
    ```

    ### Dynamic Link Creation

    In `app.py`, dynamic link generation is done by iterating over `dash.page_registry`:

    ```python
    children=[
        create_nav_link(
            icon=page["icon"], label=page["name"], href=page["path"]
        )
        for page in dash.page_registry.values()
        if page["path"].startswith("/chapter2")
    ],
    ```

    """
),
    ]
)
