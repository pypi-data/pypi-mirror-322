from pyodm.model.definition import Attribute


class CreationDateTime(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("CreationDateTime")