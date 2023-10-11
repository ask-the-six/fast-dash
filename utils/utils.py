from urllib.parse import urlparse, urlunparse
import dash_mantine_components as dmc
from dash import Output, Input, clientside_callback, html, dcc, page_container, State
from dash_iconify import DashIconify

def get_favicon_url(website_url):
    parsed_url = urlparse(website_url)
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))
    
    # Ensure there's a "/" at the end before appending favicon.ico
    if not base_url.endswith('/'):
        base_url += '/'
    
    favicon_url = f"{base_url}favicon.ico"
    return favicon_url





