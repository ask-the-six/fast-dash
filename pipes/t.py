import requests
from dataclasses import dataclass, field
from typing import Dict, Any
from dataclasses_json import dataclass_json, Undefined, CatchAll

# Define the dataclass to handle the API response with extra fields
@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class APIResponse:
    # Define expected fields (replace with actual fields you expect, if any)
    # Catch-all for unknown fields
    unknown_fields: CatchAll = field(default_factory=dict)

# Make the request
url = "https://odin.tradoc.army.mil/dotcms/api/content/_search"
payload = {
    "limit": 20,
    "offset": 40,
    "query": "+contentType:WegCard +live:true +deleted:false +conhost:8a7d5e23-da1e-420a-b4f0-471e7da8ea2d",
    "sort": "score"
}

response = requests.post(url, json=payload)

# Parse response with the dataclass
if response.status_code == 200:
    data = response.json()
    api_response = APIResponse.from_dict(data)
    print(api_response)
else:
    print(f"Request failed with status code {response.status_code}")

