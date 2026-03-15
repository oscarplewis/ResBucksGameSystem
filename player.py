from roles import Role
from occupations import Occupation, Ghost, OccupationError, GhostHarvester
import json, jsonpickle
from collections import defaultdict

class Player():
    game_information_filepath = 'game_information.json'

    def __init__(self, name:str) -> None:
        self.name:str = name
        self.previous_repr:dict = {}
        self.role:Role = None
        self.occupation:Occupation = None
        self.res_bucks:int = None
        self.ghostly_res_bucks:int = None
        self.ectoplasm:int = None
        self.maggots:dict = defaultdict(int)
        self.crops:dict = defaultdict(int)
        self._updateJson(append=True)
    
    def setRole(self, role:Role):
        self.role = role
        self._updateJson()
    
    def setOccupation(self, occupation:Occupation):
        self.occupation = occupation
        self._updateJson()

    def addResBucks(self, number:int) -> tuple[int, int]:
        """
        Add some 'number' of Res-Bucks to your wallet. If you are a Ghost Harvester (Occupation),
        use negative numbers to indicate that you are using Ghostly Res-Bucks in the transaction. If
        you are a Ghost, Ghostly Res-Bucks will be used automatically.
        
        The function will return your current wallet quantities: Res-Bucks first, Ghostly Res-Bucks second.
        """
        if (self.occupation is not Ghost) and ((self.occupation is not GhostHarvester)):
            if number < 0:
                raise OccupationError("Only Ghost Harvesters and Ghosts can use Ghostly Res Bucks, silly!")
            else:
                self.res_bucks += number
        elif (self.occupation is GhostHarvester):
            if number > 0:
                self.res_bucks += number
            if number < 0:
                self.ghostly_res_bucks += number
        elif (self.occupation is Ghost):
            if number < 0:
                raise OccupationError("You're a Ghost. You can't use normal Res-Bucks, unfortunately!")
            else:
                self.ghostly_res_bucks += number
        
        self._updateJson()

        return self.res_bucks, self.ghostly_res_bucks
    
    def subtractResBucks(self, number:int) -> None:
        """
        Pay some 'number' of Res Bucks out of your wallet. If you are a Ghost Harvester (Occupation),
        use negative numbers to indicate that you are using Ghostly Res-Bucks in the transaction. If
        you are a Ghost, Ghostly Res-Bucks will be used automatically.
        
        The function will return your current wallet quantities: Res-Bucks first, Ghostly Res-Bucks second.
        """
        if (self.occupation is not Ghost) and ((self.occupation is not GhostHarvester)):
            if number < 0:
                raise OccupationError("Only Ghost Harvesters and Ghosts can use Ghostly Res Bucks, silly!")
            else:
                self.res_bucks -= number
        elif (self.occupation is GhostHarvester):
            if number > 0:
                self.res_bucks -= number
            if number < 0:
                self.ghostly_res_bucks -= number
        elif (self.occupation is Ghost):
            if number < 0:
                raise OccupationError("You're a Ghost. You can't use normal Res-Bucks, unfortunately!")
            else:
                self.ghostly_res_bucks -= number

        self._updateJson()
    
    def passMission(self) -> None:
        """Play a Pass card on the mission or heist you're on."""
        try:
            self.role.passMission()
        except AttributeError:
            print(f"Your role is currently {self.role}, and can't pass or fail missions!")
    
    def failMission(self) -> None:
        """Play a Fail card on the mission or heist you're on. Be careful!"""
        try:
            self.role.failMission()
        except AttributeError:
            print(f"Your role is currently {self.role}, and can't pass or fail missions!")
    
    def _updateJson(self, append:bool=False) -> None:
        with open(Player.game_information_filepath, 'r+') as file:
            ### LOAD INPUT
            game_information = json.load(file)
            # serialize Player object to JSON string, and then load it as Python dict
            json_repr_dict = json.loads(jsonpickle.encode(self, warn=True))
            # checks if this is the first time we're loading the Player object
            if append:
                game_information['player_list'].append(json_repr_dict)
                if hasattr(self, 'role'):
                    game_information['current_roles'].append(json_repr_dict['role'])
            else:
                # if not, find the previous object and update it
                for i in range(len(game_information['player_list'])):
                    player = game_information['player_list'][i]
                    if self.previous_repr == player:
                        # set reference to updated value
                        game_information['player_list'][i] = json_repr_dict
                        if hasattr(self, 'role'):
                            # if a role has yet been assigned
                            if len(game_information['current_roles']) > i:
                                # and if the list of roles is already filled up to the point
                                # of this player's position in the 'current_players' list,
                                # then set the role to this player's role
                                game_information['current_roles'][i] = json_repr_dict['role']
                            else:
                                # if the list of roles is NOT filled up to the point of this
                                # player, then either there are some players before them or
                                # the list is empty; we first fill the other players' unassigned
                                # roles with default -1, and then append this player's role
                                max_index_filled = len(game_information['current_roles']) - 1
                                for j in range(max_index_filled + 1, i):
                                    game_information['current_roles'].append(int(-1))
                                game_information['current_roles'].append(json_repr_dict['role'])
                        break
            self.previous_repr = json_repr_dict

            ### WRITE OUTPUT
            file.seek(0) # reset pointer to beginning of file so we overwrite instead of append
            json.dump(game_information, file, indent=2)

