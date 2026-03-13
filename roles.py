from vars import Team, StatusCards, WinConditions
import json

class RoleError(Exception):
    """Exception raised when a Role tries to do something forbidden to them."""
    pass

class Role():
    def __init__(self, name:str, description:str, team:Team, importance:int, guessable:bool=False) -> None:
        self.name:str = name
        self.description:str = description
        self.team:Team = team
        self.importance:int = importance
        self.guessable:bool = guessable
    
    def __repr__(self) -> str:
        return f"{self.name} ({self.team.value}) [{self.importance}] : {self.description}"
    
    def getWinCondition(self) -> str:
        return self.team.getWinCondition()

    @staticmethod
    def passMission() -> None:
        with open('missions.json', 'r') as file:
            missions = json.load(file)
        with open('missions.json', 'w') as file:
            missions['go_pile'].append(StatusCards.Pass.value)
            json.dump(missions, file)
    
    @staticmethod
    def failMission() -> None:
        with open('missions.json', 'r') as file:
            missions = json.load(file)
        with open('missions.json', 'w') as file:
            missions['go_pile'].append(StatusCards.Fail.value)
            json.dump(missions, file) 

##################################
########### RESISTANCE ###########
##################################
    
class Res(Role):
    def __init__(self) -> None:
        name = "Res"
        description = "This is the typical Res role from the “normal” game of The Resistance / Avalon. The Res begins the game with no knowledge, can only pass missions, and can either pass or fail heists."
        team = Team.Blue
        importance = 1
        super().__init__(name, description, team, importance)

    @staticmethod
    def failMission() -> None:
        raise RoleError("Res can only pass missions!")

#############################
########### SPIES ###########
#############################

class Spy(Role):
    def __init__(self) -> None:
        name = "Spy"
        description = "This is the typical Spy role from the “normal” game of The Resistance / Avalon. This role begins the game knowing who the other Spies are. This role can either pass or fail missions and heists."
        team = Team.Red
        importance = 1
        super().__init__(name, description, team, importance)
