class Occupation():
    pass

class Ghost(Occupation):
    pass

class GhostHarvester(Occupation):
    pass

class OccupationError(Exception):
    """Exception raised when an Occupation tries to do something forbidden to them."""
    pass