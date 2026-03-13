from enum import Enum

class bind:
    bound_methods = {}

    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        def wrapper(wrapped_self, *args, **kwargs):
            return self.bound_methods[(func.__qualname__, wrapped_self.name)](wrapped_self, *args, **kwargs)
        
        # Store the actual function mapped by the qualified name of the function and the enum member name
        self.bound_methods[(func.__qualname__, self.name)] = func
        return wrapper

# enumeration has "name" as the first entry and "value" as the second
# access by e.g. Team.red.name, Team.red.value
class Team(Enum):
    Blue = 'The Resistance'
    Red = 'The Spies'
    Green = 'The Malcapher Syndicate [archaic]'
    Yellow = 'The Yellow Team'
    Gray = 'The Adversarial Dome'

    def getWinCondition(self) -> str:
        match self:
            case Team.Blue:
                return WinConditions.Blue.value
            case Team.Red:
                return WinConditions.Red.value
            case Team.Green:
                return WinConditions.Green.value
            case Team.Yellow:
                return WinConditions.Yellow.value
            case Team.Gray:
                return WinConditions.Gray.value
            case _:
                raise ValueError("Team is not recognized!")
        


class WinConditions(Enum):
    Blue = "The Resistance win immediately if there are a majority of successful missions on the mission board."
    Red = "The Spies win immediately if there are a majority of failed missions on the mission board."
    Green = "The Malcapher Syndicate [archaic] wins if they obtain 5 success tokens, or if the game ends after at most N rounds."
    Yellow = "The Yellow Team wins if any of the Yellow Team players meet their win condition."
    Gray = "The Adversarial Dome has no win condition: it cannot win the game, but can only oppose players."

class StatusCards(Enum):
    Pass = 1
    Fail = 0
