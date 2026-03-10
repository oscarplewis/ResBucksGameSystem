class Bowl:
    """Basic container class."""
    def __init__(self, name:str, bowl_type:str='list') -> None:
        self.name = name
        if bowl_type == 'list':
            self.objects:list = [] # type: ignore
        elif bowl_type == 'dict':
            self.objects:dict = {} # type: ignore
        else:
            raise ValueError("'bowl_type' must be either a 'list' or 'dict'!")
        self.n_objects = 0
        
    def add(self, object:dict|list|tuple) -> None:
        if type(self.objects) is list:
            self.objects.append(object)
        elif type(self.objects) is dict:
            if type(object) is dict:
                self.objects.update(object)
            elif type(object) is list or tuple:
                self.objects.update({object[0]: object[1]})
            else:
                raise TypeError(f"'object' type must be a tuple, list, set, or dict if {self.name}.objects is stored as dict!")
        self.n_objects += 1
    
    def get(self, key:int|str):
        return self.objects[key] # type: ignore # raises error bc self.objects type is not specified here
    
    def __repr__(self):
        return f'{self.name} (contains {self.n_objects})'

class Lesson:
    def __init__(self, name:str, description:str=''):
        self.name = name
        if type(description) is not str:
            raise TypeError("'description' must be a string")
        self.description = description
    
    def addDescription(self, description:str) -> None:
        if type(description) is not str:
            raise TypeError("'description' must be a string")
        if self.description:
            raise ValueError("'description' already has a value! Use 'changeDescription' if you wish to change it")
        self.description = description

    def getDescription(self) -> str:
        return self.description
    
    def changeDescription(self, description:str) -> None:
        if type(description) is not str:
            raise TypeError("'description' must be a string")
        self.description = description
    
    def __repr__(self):
        return f"{self.name} (Lesson): {self.description}"
    
class LessonBowl(Bowl):
    """Container class specific for the Bowl of Lessons."""
    def __init__(self, name:str):
        super().__init__(name, 'dict')

    def add(self, object:Lesson|list[Lesson]|tuple[Lesson]|dict[str, str]):
        if type(object) is Lesson:
            self.objects.update({object.name: object.description})
            self.n_objects += 1
        elif type(object) is dict:
            self.objects.update(object)
            self.n_objects = len(self.objects.keys())
        else:
            for obj in object: # type: ignore
                self.objects.update({obj.name: obj.description})
            self.n_objects += len(object) # type: ignore

    def get(self, key:str) -> Lesson:
        return Lesson(key, self.objects[key])

BowlOfLessons = LessonBowl('BowlOfLessons')
lessons = {
    'TestLesson' : 'Lesson description',
}

