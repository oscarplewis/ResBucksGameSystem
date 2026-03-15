import json
from vars import StatusCards

missions_template = {
    "go_pile" : [],
    "discard_pile" : [],
}

game_information_template = {
    "player_list" : [], # list of Player objects correspond to all current players
    "previous_roles" : [], # list of roles in the previous game, ordered according to the list of players
    "previous_occupations" : [], # list of occupations in the previous game, ordered according to the list of players
    "current_roles" : [], # list of roles in the current game, ordered according to the list of players
    "current_occupations" : [],
}

with open('missions.json', 'w') as file:
    json.dump(missions_template, file, indent=2)
with open('game_information.json', 'w') as file:
    json.dump(game_information_template, file, indent=2)
