import dash_mantine_components as dmc
from collections import defaultdict
from dash import Output, Input, clientside_callback, html, dcc, page_container, State, callback
from dash_iconify import DashIconify

import yaml

def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
ui_configs = load_yaml_config("ui-config.yaml")
default_header_data = ui_configs["header_data"]
default_theme = ui_configs["theme"]
defined_icon_categories = ui_configs["sections"]
  # This is your odict_values output
DEFAULT_ICON = "fa-solid:folder"



# Retrieve values from the YAML or use the defaults:
   
def assign_missing_icons(nav_data, defined_icon_categories):
    """
    For each section and page in nav_data, checks if there's a corresponding icon.
    If not, assigns the default icon to that section/page.
    
    Args:
    - nav_data (list): List of navigation data.
    - defined_icon_categories (dict): Dictionary with icons for sections.
    
    Returns:
    - tuple: Two dictionaries. The first with icons for each section and the second for each page.
    """
    section_icons = {}
    page_icons = {}
    
    for entry in nav_data:
        section = entry.get("section")
        name = entry.get("name")
        
        # Check for section icon
        if section and section not in section_icons:
            section_icons[section] = defined_icon_categories.get(section, DEFAULT_ICON)
        
        # Check for page icon
        if name:
            page_icons[name] = entry.get("icon", DEFAULT_ICON)

    return section_icons, page_icons




def create_home_link(label):
    """
    Create a home anchor link with specified label.
    
    Args:
    - label (str): The display text for the anchor link.
    
    Returns:
    - dmc.Anchor: The anchor link pointing to the home page.
    """
    return dmc.Anchor(
        label,
        size="xl",
        href="/",
        underline=False,
    )



def create_header_link(icon, href, size=22, color="indigo"):
    """
    Create a header anchor link with a specified icon.
    
    Args:
    - icon (str): Iconify string to represent the icon.
    - href (str): Target URL for the anchor link.
    - size (int, optional): Size of the icon. Defaults to 22.
    - color (str, optional): Color of the icon. Defaults to "indigo".
    
    Returns:
    - dmc.Anchor: The anchor link with the given icon pointing to the specified href.
    """
    return dmc.Anchor(
        dmc.ThemeIcon(
            DashIconify(
                icon=icon,
                width=size,
            ),
            variant="outline",
            radius=30,
            size=36,
            color=color,
        ),
        href=href,
        target="_blank",
    )


def create_header(nav_data, header_data=default_header_data):
    """
    Create the header with the provided navigation data and optional header data.
    
    Args:
    - nav_data (list): A list of navigation items derived from `dash.page_registry.values()`.
    - header_data (dict, optional): A dictionary specifying the header configurations.

    If header_data is not provided, it defaults to a predefined set of header items.

    Example for header_data:
    {
        "home_links": {
            "large": "Dash Mantine Components",
            "small": "DMC"
        },
        "header_links": [
            {"icon": "radix-icons:github-logo", "url": "https://github.com/some-repo"},
            ...
        ]
    }
    
    Returns:
    - dmc.Header: The header created with the provided navigation and header data.
    """
    return dmc.Header(
        height=70,
        fixed=True,
        px=25,
        children=[
            dmc.Stack(
                justify="center",
                style={"height": 70},
                children=dmc.Grid(
                    children=[
                        dmc.Col(dmc.Burger(id="burger-button", opened=False, mr="xl"), span="content"),
                        dmc.Col(
                            [
                
                                dmc.MediaQuery(
                                    create_home_link(header_data["home_links"]["large"]),
                                    smallerThan="lg",
                                    styles={"display": "none"},
                                ),
                                dmc.MediaQuery(
                                    create_home_link(header_data["home_links"]["small"]),
                                    largerThan="lg",
                                    styles={"display": "none"},
                                ),
                            ],
                            span="content",
                            pt=12,
                        ),
                        dmc.Col(
                            span="auto",
                            children=dmc.Group(
                                position="right",
                                spacing="xl",
                                children=[
                                    dmc.MediaQuery(
                                        dmc.Select(
                                            id="select-component",
                                            style={"width": 250},
                                            placeholder="Search",
                                            nothingFound="No match found",
                                            searchable=True,
                                            clearable=True,
                                            data=[
                                                {
                                                    "label": component["name"],
                                                    "value": component["path"],
                                                }
                                                for component in nav_data
                                                if component["name"]
                                                not in ["Home", "Not found 404"]
                                            ],
                                            icon=DashIconify(
                                                icon="radix-icons:magnifying-glass"
                                            ),
                                        ),
                                        smallerThan="md",
                                        styles={"display": "none"},
                                    ),
                                    *[
                                        create_header_link(link["icon"], link["url"])
                                        for link in header_data["header_links"]
                                    ],
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="radix-icons:blending-mode", width=22
                                        ),
                                        variant="outline",
                                        radius=30,
                                        size=36,
                                        color="yellow",
                                        id="color-scheme-toggle",
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
def create_smol_side_nav_content(nav_data, navbar_icons={}, page_icons={}):
    """
    Create the content for the small side navigation based on provided navigation data.
    """
    return create_side_nav_content(nav_data, navbar_icons=navbar_icons, page_icons=page_icons, collapse_to_icons_store=True)

def create_lg_side_nav_content(nav_data, navbar_icons={}, page_icons={}):
    """
    Create the content for the large side navigation based on provided navigation data.
    """
    return create_side_nav_content(nav_data, navbar_icons=navbar_icons, page_icons=page_icons, collapse_to_icons_store=False)

def create_side_nav_content(nav_data, navbar_icons={}, page_icons={}, collapse_to_icons_store=True):
    """
    Create the content for the side navigation based on provided navigation data.
    
    Args:
    - nav_data (list): List of navigation data. Derived typically from `create_appshell(dash.page_registry.values())`.
                      Each entry can contain 'name', 'path', and optionally a 'section'.

    - navbar_icons (dict, optional): Dictionary specifying icons for different sections.

    Example for main_links_data:
    [
        {"icon": "material-symbols:rocket-launch-rounded", "name": "Getting Started", "path": "/getting-started"},
        {"icon": "material-symbols:style", "name": "Styles API", "path": "/styles-api"},
        ...
    ]
    
    Returns:
    - dmc.Stack: Stack component containing main navigation links and sections.
    """
    if collapse_to_icons_store:
        collapse_to_icons = collapse_to_icons_store
    else:
        collapse_to_icons = False
    sections = defaultdict(list)
    for entry in nav_data:
        section = entry.get("section")
        if section:
            sections[section].append((entry["name"], entry["path"]))
    collapsible_links = []

    for section, items in sorted(sections.items()):
        child_links = []
        
        for item in items:
            name, path = item
            page_icon = page_icons.get(name, DEFAULT_ICON)
            # If navbar is collapsed, show only icons; otherwise, show names too
            if collapse_to_icons:
                child_links.append(
                    dmc.NavLink(
                        label=None, 
                        href=path, 
                        icon=DashIconify(icon=page_icon, width=20),
                        styles={"root": {"height": 32}}
                    )
                )
            else:
                child_links.append(
                    dmc.NavLink(
                        label=name, 
                        href=path, 
                        icon=DashIconify(icon=page_icon, width=20),
                        styles={"root": {"height": 32}}
                    )
                )

        section_icon = navbar_icons.get(section, DEFAULT_ICON)
        # Only make sections collapsible
        collapsible_links.append(
            dmc.NavLink(
                label=section if not collapse_to_icons else None,
                icon=DashIconify(icon=section_icon, width=15),
                childrenOffset=0 if collapse_to_icons else 25,
                opened=False,
                children=child_links,
            )
        )

    return dmc.Stack(spacing=0, children=[*collapsible_links, dmc.Space(h=20)])




def create_side_navbar(nav_data):
    """
    Create a sidebar navigation with specified navigation data.
    
    Args:
    - nav_data (dict): Data for creating the side navigation bar.
    
    Returns:
    - dmc.Navbar: The side navigation bar component.
    """
    icons_dict, page_icons_dict = assign_missing_icons(nav_data, defined_icon_categories)
    return dmc.Navbar(
        fixed=True,
        id="components-navbar",
        width={"base": 300},
        children=[
        dmc.SimpleGrid(
    id='smol_nav',
    cols=1,
    style={'display': 'none'},
            children=[
                 create_smol_side_nav_content(nav_data, navbar_icons=icons_dict, page_icons=page_icons_dict)
            ]
        ),
        dmc.SimpleGrid(
    cols=1,
    id='big_nav',
    style={'display': 'block'},
            children=[
                create_lg_side_nav_content(nav_data, navbar_icons=icons_dict, page_icons=page_icons_dict)
            ]
        )
        ]
    )



def create_appshell(nav_data, theme_data=default_theme):
    """
    Create the app shell with the provided navigation data and optional theme data.
    
    Args:
    - nav_data (list): A list derived from `create_appshell(dash.page_registry.values())`.
    - theme_data (dict, optional): A dictionary specifying the theme properties. 

    If theme_data is not provided, it defaults to a predefined theme.

    Example for theme_data:
    {
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            ...
        }
    }
    
    Returns:
    - dmc.MantineProvider: The app shell created with the provided theme and navigation data.
    """
    
    return dmc.MantineProvider(
        dmc.MantineProvider(
            theme=theme_data,
            inherit=True,
            children=[
                dcc.Store(id="theme-store", storage_type="local"),
                dcc.Location(id="url", refresh="callback-nav"),
                dmc.NotificationsProvider(
                    [
                        create_header(nav_data),
                        create_side_navbar(nav_data),
                        dmc.AppShell(
                        html.Div(
                            dmc.Container(size="lg", pt=90, children=page_container),
                            id="wrapper",
                        ),)
                    ]
                ),
            ],
        ),
        theme={"colorScheme": "light"},
        id="mantine-docs-theme-provider",
        withGlobalStyles=True,
        withNormalizeCSS=True,
    )




clientside_callback(
    """ function(data) { return data } """,
    Output("mantine-docs-theme-provider", "theme"),
    Input("theme-store", "data"),
)

clientside_callback(
    """function(n_clicks, data) {
        if (data) {
            if (n_clicks) {
                const scheme = data["colorScheme"] == "dark" ? "light" : "dark"
                return { colorScheme: scheme } 
            }
            return dash_clientside.no_update
        } else {
            return { colorScheme: "light" }
        }
    }""",
    Output("theme-store", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("theme-store", "data"),
)


clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
    }
    """,
    Output("url", "pathname"),
    Input("select-component", "value"),
)

clientside_callback(
    """
    function(opened, currentWidth) {
        if(opened) {
            return { base: 300 };  
        } else {
            return { base: 75 };  // Restore the original width when burger is closed
        }
    }
    """,
    Output("components-navbar", "width"),
    Input("burger-button", "opened"),
    State("components-navbar", "width")
)


clientside_callback(
    """
    function(opened) {
        if(opened) {
            return [{'display': 'none'}, {'display': 'block'}];  // smol_nav hidden, big_nav shown
        } else {
            return [{'display': 'block'}, {'display': 'none'}];  // smol_nav shown, big_nav hidden
        }
    }
    """,
    [Output('smol_nav', 'style'), Output('big_nav', 'style')],
    [Input('burger-button', 'opened')]
)

