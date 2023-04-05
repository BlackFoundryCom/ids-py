from collections import defaultdict
from importlib.resources import files
import os
from fontTools import unicodedata


DATA_DIR = "ids_data"

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
            # print('char', char)
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

        data_dir = files("ids_py.ids_data")
        source_paths = [p for p in data_dir.iterdir() if p.suffix == ".txt"]

        for path in source_paths:
            with open(path, "r", encoding="utf-8") as file:
                data = file.read()

            for line in data.splitlines()[1:]:
                character = Character()
                character.read(line)
                self._characters[character.character] = character
                for component in character.composition:
                    self._component_to_characters[component].append(character.character)
        print(len(self._characters))

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
                        composition += " {%s:"%_component.character
                        composition += self.get_flatten_composition(
                            _component.character, composition
                        )
                        composition += "} "
                    else:
                        composition += _component.character
                else:
                    composition += component
        return composition 

    def get_characters_used_by(self, component, structure = None):
        characters = self._component_to_characters.get(component, "")
        if structure is None:
            return characters
        else:
            structures = defaultdict(list)
            for character in characters:
                s = self.get_character_structure(character)
                if structure != "all" and s != structure:
                    continue
                structures[s].append(character)
            return structures


if __name__ == "__main__":
    ids = IDS()
    print("----")
    print("Composition")
    for char in "吃僰汄嚻忁圗渁":
        print(char, "->", ids.get_character_composition(character=char))
        print("\n")

    print("\n----")
    print("Structure")
    for char in "吃僰汄畵忁":
        print(char, "->", ids.get_character_structure(character=char))
        print("\n")

    print("\n----")
    print("Flatten composition")
    for char in "僰嚻忁圗渁辔僲":
        print(char, "->", ids.get_flatten_composition(char))
        print("\n")

    print("\n----")
    print("Used by")
    for char in "人⿶⿲水⿳凼":
        print(char, "->", "".join(ids.get_characters_used_by(component=char)))
        print("\n")

    for char in "耳":
        used_by = ids.get_characters_used_by("耳", structure = "all")
        for k, v in used_by.items():
            print(f"{char}{k}", "->", "".join(sorted(v)))

    print("\n----")
    print("Similar")
    for char in "吃僰汄凼洞渆嘂壱请豪耿":
        print(char, ":")
        similar = ids.get_character_similar_to(character=char)
        for k, v in similar.items():
            print("\t", "".join(k), ":", "".join(v))
        print("\n")

    print("\n----")
    for char in ids.get_characters_used_by(component="\t"):
        print(char, "->", ids.get_character_composition(char))

