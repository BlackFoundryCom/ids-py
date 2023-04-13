import json
import os
from collections import defaultdict
from importlib.resources import files

from fontTools import unicodedata


STRUCTURE = "IDEOGRAPHIC DESCRIPTION CHARACTER"

DATA_DIR = files("ids_py.data")

CHARACTERS_COMPOSITION_PATH = DATA_DIR.joinpath('IDS_characters_composition.json')

COMPONENTS_TO_CHARACTERS_PATH = DATA_DIR.joinpath('IDS_components_to_characters.json')

with open(CHARACTERS_COMPOSITION_PATH, "r", encoding="utf-8") as file:
    characters = json.loads(file.read())

with open(COMPONENTS_TO_CHARACTERS_PATH, "r", encoding="utf-8") as file:
    components_to_characters = json.loads(file.read())


def _component_order(character):
    compo_order = []
    structure = ""
    composition = character.get("composition", "")
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


def _structure(character):
    structure = ""
    for char in character.get("composition"):
        if STRUCTURE in unicodedata.name(char):
            structure += char
    return structure


def get_character_structure(character):
    _character = characters.get(character, None)
    if _character is not None:
        return _structure(_character)


def get_character_composition(character):
    _character = characters.get(character, None)
    if _character is not None:
        return _character.get("composition", "")


def get_characters_used_by(component, structure=None):
    chars = components_to_characters.get(component, "")
    if structure is None:
        return chars
    else:
        structures = defaultdict(list)
        for char in chars:
            s = get_character_structure(char)
            if structure != "all" and s != structure:
                continue
            structures[s].append(char)
        return structures


def get_character_similar_to(character):
    _character = characters.get(character, None)
    similar = defaultdict(list)
    if _character is not None:
        for index, compo in enumerate(_component_order(_character)):
            characters_used_by = get_characters_used_by(compo[0])
            for character_used_by in characters_used_by:
                _character_used_by = characters.get(character_used_by, None)
                compo_order = _component_order(_character_used_by)
                if index < len(compo_order):
                    if compo == compo_order[index]:
                        similar[compo].append(character_used_by)
    return similar


def get_flatten_composition(character, composition=""):
    composition = ""
    _character = characters.get(character, None)
    if _character is not None:
        for component in _character.get("composition", ""):
            _component = characters.get(component, None)
            if _component is not None:
                if len(_component.get("composition")) > 1:
                    composition += " {%s:" % _component.get(character, "")
                    composition += get_flatten_composition(
                        _component.get(character, ""), composition
                    )
                    composition += "} "
                else:
                    composition += _component.get("character")
            else:
                composition += component
    return composition
