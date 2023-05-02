import json
import os
from collections import defaultdict
from importlib.resources import files

from fontTools import unicodedata


STRUCTURE = "IDEOGRAPHIC DESCRIPTION CHARACTER"

DATA_DIR = files("ids_py.data")

CHARACTERS_COMPOSITION_PATH = DATA_DIR.joinpath("IDS_characters_composition.json")

COMPONENTS_TO_CHARACTERS_PATH = DATA_DIR.joinpath("IDS_components_to_characters.json")

with open(CHARACTERS_COMPOSITION_PATH, "r", encoding="utf-8") as file:
    characters = json.loads(file.read())

with open(COMPONENTS_TO_CHARACTERS_PATH, "r", encoding="utf-8") as file:
    components_to_characters = json.loads(file.read())


def _component_order(composition):
    compo_order = []
    structure = ""
    if "\t" in composition:
        composition = composition.split("\t")[0]
    for char in composition:
        try:
            name = unicodedata.name(char)
        except:
            continue
        if not name:
            continue
        if STRUCTURE in name:
            structure = char
        else:
            compo_order.append((char, structure))
    return compo_order


def _structure(composition):
    structure = ""
    for char in composition:
        if STRUCTURE in unicodedata.name(char):
            structure += char
    return structure


def structure(character):
    composition = characters.get(character, None)
    return _structure(composition)


def composition(character):
    composition = characters.get(character, None)
    return composition


def used_by(component, structure=None):
    chars = components_to_characters.get(component, "")
    if structure is None:
        return chars
    else:
        structures = defaultdict(list)
        for char in chars:
            composition = characters.get(char, None)
            s =  _structure(composition)
            if structure != "all" and s != structure:
                continue
            structures[s].append(char)
        return structures


def similar_to(character):
    composition = characters.get(character, None)
    similar = defaultdict(list)
    if composition is not None:
        for index, compo in enumerate(_component_order(composition)):
            characters_used_by = used_by(compo[0])
            for character_used_by in characters_used_by:
                _character_used_by = characters.get(character_used_by, None)
                compo_order = _component_order(_character_used_by)
                if index < len(compo_order):
                    if compo == compo_order[index]:
                        similar[compo].append(character_used_by)
    return similar


def flatten_composition(character, character_composition=""):
    character_composition = ""
    composition = characters.get(character, None)
    if composition is not None:
        for component in composition:
            _component = characters.get(component, None)
            if _component is not None:
                if len(_component) > 1:
                    character_composition += " {%s:" % component
                    character_composition += flatten_composition(
                        component, character_composition
                    )
                    character_composition += "} "
                else:
                    character_composition += component
            else:
                character_composition += component
    return character_composition
