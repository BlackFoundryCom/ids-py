import json
import os
from collections import defaultdict

import requests

GITLAB_CHISE_IDS_URL = "https://gitlab.chise.org/CHISE/ids/"
MASTER_RAW = f"{GITLAB_CHISE_IDS_URL}-/raw/master/"

IDS_UCS_URLs = [
    "IDS-UCS-Basic",
    "IDS-UCS-Ext-A",
    "IDS-UCS-Ext-B-1",
    "IDS-UCS-Ext-B-2",
    "IDS-UCS-Ext-B-3",
    "IDS-UCS-Ext-B-4",
    "IDS-UCS-Ext-B-5",
    "IDS-UCS-Ext-B-6",
    "IDS-UCS-Ext-C",
    "IDS-UCS-Ext-D",
    "IDS-UCS-Ext-E",
    "IDS-UCS-Ext-F",
    "IDS-UCS-Ext-G",
    "IDS-UCS-Ext-H",
    "IDS-UCS-Compat-Supplement",
    "IDS-UCS-Compat"
]

OUTPUT_DIR = "src/ids_py/ids_data"
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

character_composition_output_path = os.path.join(
    OUTPUT_DIR, "IDS_characters_composition.json"
)
components_to_characters_output_path = os.path.join(
    OUTPUT_DIR, "IDS_components_to_characters.json"
)

characters = {}
component_to_characters = defaultdict(list)

for filename in IDS_UCS_URLs:
    url = f"{MASTER_RAW}{filename}.txt"
    response = requests.get(url)
    content = response.text

    for line in content.splitlines()[1:]:
        parts = line.split("\t")
        _unicode, _character = parts[:2]
        _composition = "\t".join(parts[2:])
        characters[_character] = dict(
            character=_character, unicode=_unicode, composition=_composition
        )
        for component in _composition:
            component_to_characters[component].append(_character)

with open(character_composition_output_path, "w", encoding="utf-8") as file:
    json.dump(characters, file, indent=2, ensure_ascii=False)

with open(components_to_characters_output_path, "w", encoding="utf-8") as file:
    json.dump(component_to_characters, file, indent=2, ensure_ascii=False)
