import json
import os
from collections import defaultdict

import requests

GITLAB_CHISE_IDS_URL = "https://gitlab.chise.org/CHISE/ids/"

IDS_UCS_URLs = dict(
    IDS_UCS_Basic_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Basic.txt",
    IDS_UCS_EXT_A_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-A.txt",
    IDS_UCS_EXT_B_1_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-B-1.txt",
    IDS_UCS_EXT_B_2_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-B-2.txt",
    IDS_UCS_EXT_B_3_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-B-3.txt",
    IDS_UCS_EXT_B_4_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-B-4.txt",
    IDS_UCS_EXT_B_5_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-B-5.txt",
    IDS_UCS_EXT_B_6_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-B-6.txt",
    IDS_UCS_EXT_C_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-C.txt",
    IDS_UCS_EXT_D_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-D.txt",
    IDS_UCS_EXT_E_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-E.txt",
    IDS_UCS_EXT_F_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-F.txt",
    IDS_UCS_EXT_G_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-G.txt",
    IDS_UCS_EXT_H_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Ext-H.txt",
    IDS_UCS_COMPAT_SUPPLEMENT_URL=GITLAB_CHISE_IDS_URL
    + "-/raw/master/IDS-UCS-Compat-Supplement.txt",
    IDS_UCS_COMPAT_URL=GITLAB_CHISE_IDS_URL + "-/raw/master/IDS-UCS-Compat.txt",
)

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

for filename, url in IDS_UCS_URLs.items():
    response = requests.get(url)
    data = response.content
    content = data.decode("utf-8")

    for line in content.splitlines()[1:]:
        splitedline = line.split("\t")
        _unicode, _character = splitedline[:2]
        _composition = "\t".join(splitedline[2:])
        characters[_character] = dict(
            character=_character, unicode=_unicode, composition=_composition
        )
        for component in _composition:
            component_to_characters[component].append(_character)

with open(character_composition_output_path, "w", encoding="utf-8") as file:
    json.dump(characters, file, indent=2, ensure_ascii=False)

with open(components_to_characters_output_path, "w", encoding="utf-8") as file:
    file.write(json.dumps(component_to_characters, indent=4, separators=(",", ": ")))
