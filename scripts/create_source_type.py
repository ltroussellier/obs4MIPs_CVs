import json
import os
from pathlib import Path

import esgvoc.api as ev
import requests

# URLs of the JSON files on GitHub
json_url = "https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/refs/heads/master/obs4MIPs_source_type.json"

# Directory where the JSON files will be saved
save_dir = "obs4MIPs_source_type"

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)


# Function to fetch and load JSON data from a URL
def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return response.json()


data = fetch_json(json_url)["source_type"]

known_sources_in_universe = ev.get_all_terms_in_data_descriptor("obs_type")
print(known_sources_in_universe)
for item in data:
    found_item = None
    for sour in known_sources_in_universe:
        if sour.drs_name == item:
            found_item = sour
            break

    if found_item is None:
        print(item, "not found in universe")
    else:
        # Create json file
        dict_to_save = {
            "@context": "000_context.jsonld",
            "id": found_item.id,
            "type": found_item.type,
        }
        # print(dict_to_save)
        with open(Path(save_dir) / f"{found_item.id}.json", "w") as f:
            json.dump(dict_to_save, f, indent=4)
