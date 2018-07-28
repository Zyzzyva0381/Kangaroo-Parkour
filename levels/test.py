import json
f = open("level_1.json", "r")
text = f.read()
print(text + "\n")
loaded = json.loads(text)
print(loaded)