from collections import defaultdict

import requests
from fontTools import unicodedata

from URL import IDS_UCS_URLs

STRUCTURE = "IDEOGRAPHIC DESCRIPTION CHARACTER"


class Character:
    def read(self, line):
        splitedline = line.split("\t")
        self.unicode, self.character = splitedline[:2]
        self.composition = "\t".join(splitedline[2:])

    @property
    def component_order(self):
        compo_order = []
        structure = ""
        composition = self.composition
        if "\t" in self.composition:
            composition = self.composition.split("\t")[0]
        for char in composition:
            name = unicodedata.name(char)
            if not name:
                continue
            if STRUCTURE in name:
                structure = char
            else:
                compo_order.append((char, structure))
        return compo_order

    @property
    def structure(self):
        structure = ""
        for char in self.composition:
            if STRUCTURE in unicodedata.name(char):
                structure += char
        return structure


class IDS:
    def __init__(self):
        self._characters = {}
        self._component_to_characters = defaultdict(list)
        for filename, url in IDS_UCS_URLs.items():
            response = requests.get(url)
            data = response.content

            for line in data.decode("utf-8").splitlines()[1:]:
                character = Character()
                character.read(line)
                self._characters[character.character] = character
                for component in character.composition:
                    self._component_to_characters[component].append(character.character)

    def get_character_structure(self, character):
        _character = self._characters.get(character, None)
        if _character is not None:
            return _character.structure

    def get_character_composition(self, character):
        _character = self._characters.get(character, None)
        if _character is not None:
            return _character.composition

    def get_character_similar_to(self, character):
        _character = self._characters.get(character, None)
        similar = defaultdict(list)
        if _character is not None:
            for index, compo in enumerate(_character.component_order):
                characters_used_by = self.get_characters_used_by(compo[0])
                for character_used_by in characters_used_by:
                    _character_used_by = self._characters.get(character_used_by, None)
                    compo_order = _character_used_by.component_order
                    if index < len(compo_order):
                        if compo == compo_order[index]:
                            similar[compo].append(character_used_by)
        return similar

    def get_flatten_composition(self, character, composition=""):
        composition = ""
        _character = self._characters.get(character, None)
        if _character is not None:
            for component in _character.composition:
                _component = self._characters.get(component, None)
                if _component is not None:
                    if len(_component.composition) > 1:
                        composition += self.get_flatten_composition(
                            _component.character, composition
                        )
                    else:
                        composition += _component.character
        return composition

    def get_characters_used_by(self, component):
        return self._component_to_characters.get(component, "")


if __name__ == "__main__":
    ids = IDS()
    print("----")
    print("Composition")
    for char in "吃僰汄嚻":
        print(char, "->", ids.get_character_composition(character=char))
        print("\n")

    print("\n----")
    print("Structure")
    for char in "吃僰汄畵":
        print(char, "->", ids.get_character_structure(character=char))
        print("\n")

    print("\n----")
    print("Flatten composition")
    for char in "僰嚻忁":
        print(char, "->", ids.get_flatten_composition(char))
        print("\n")

    print("\n----")
    print("Used by")
    for char in "人⿶⿲水⿳":
        print(char, "->", "".join(ids.get_characters_used_by(component=char)))
        print("\n")

    print("\n----")
    print("Similar")
    for char in "吃僰汄凼洞渆嘂壱请":
        print(char, ":")
        similar = ids.get_character_similar_to(character=char)
        for k, v in similar.items():
            print("\t", "".join(k), ":", "".join(v))
        print("\n")
