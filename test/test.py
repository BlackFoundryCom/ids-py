import time

import ids_py as ids

print("----")
print("Composition")
for char in "吃":#侃吃僰汄嚻忁圗渁":
    response = ids.composition(character=char)
    print(char, "->", response, type(response))
    print("\n")

print("\n----")
print("Structure")
for char in "畵":#侃吃僰汄畵忁":
    response = ids.structure(character=char)
    print(char, "->", response, type(response))
    print("\n")

print("\n----")
print("Flatten composition")
for char in "吃":#侃僰嚻忁圗渁辔僲":
    response = ids.composition(char, flatten = True)
    print(char, "->", response, type(response))
    print("\n")

print("\n----")

print("Used by")

for char in "我⿶":#侃人⿶⿲水⿳凼":
    response = ids.used_by(component=char)
    print(char, "->", "".join(response), type(response))
    print("\n")

for char in "我":#耳":
    used_by = ids.used_by("我", structure="all")
    print(used_by, type(used_by))
    for k, v in used_by.items():
        print(f"{char}{k}", "->", "".join(sorted(v)))

print("\n----")

print("Similar")
start = time.time()
for char in "请":#恰吃僰汄凼洞渆嘂壱请豪耿":
    print(char, ":")
    similar = ids.similar_to(character=char)
    print(similar, type(similar))
    for k, v in similar.items():
        print("\t", "".join(k), ":", "".join(v))
    print("\n")
stop = time.time()

# print("\n----")
# for char in ids.get_characters_used_by(component="\t"):
#     print(char, "->", ids.get_character_composition(char))

print(stop - start)
