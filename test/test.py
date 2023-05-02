import time

import ids_py as ids

print("----")
print("Composition")
for char in "侃吃僰汄嚻忁圗渁":
    print(char, "->", ids.composition(character=char))
    print("\n")

print("\n----")
print("Structure")
for char in "侃吃僰汄畵忁":
    print(char, "->", ids.structure(character=char))
    print("\n")

print("\n----")
print("Flatten composition")
for char in "侃僰嚻忁圗渁辔僲":
    print(char, "->", ids.flatten_composition(char))
    print("\n")

print("\n----")

print("Used by")

for char in "侃人⿶⿲水⿳凼":
    print(char, "->", "".join(ids.used_by(component=char)))
    print("\n")

for char in "耳":
    used_by = ids.used_by("耳", structure="all")
    for k, v in used_by.items():
        print(f"{char}{k}", "->", "".join(sorted(v)))

print("\n----")

print("Similar")
start = time.time()
for char in "恰吃僰汄凼洞渆嘂壱请豪耿":
    print(char, ":")
    similar = ids.similar_to(character=char)
    for k, v in similar.items():
        print("\t", "".join(k), ":", "".join(v))
    print("\n")
stop = time.time()

# print("\n----")
# for char in ids.get_characters_used_by(component="\t"):
#     print(char, "->", ids.get_character_composition(char))

print(stop - start)
