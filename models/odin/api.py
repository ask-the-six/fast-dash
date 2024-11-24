import requests
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from dataclasses_json import dataclass_json, Undefined, CatchAll
# Define a separate class for API paths
@dataclass
class OdinPaths:
    base_url: str = "https://odin.tradoc.army.mil/dotcms/api"
    search: str = "/content/_search"
    subnav: str = "/subnav/weg"

    def get_url(self, path: str) -> str:
        return f"{self.base_url}{path}"


def search_content(
        self,
        query: str="+contentType:WegCard +live:true +deleted:false", 
        limit: int = 20, 
        offset: int = 0, 
        sort: str = "score"
    ) :
    url = OdinPaths.get_url(self.paths.search)
    payload = {
        "limit": limit,
        "offset": offset,
        "query": query,
        "sort": sort
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response
        return data
    else:
        raise Exception(f"Request failed with status code {response.status_code}")