import json

missions_template = {
    "go_pile" : [],
}

with open('missions.json', 'w') as file:
    json.dump(missions_template, file, indent=1)