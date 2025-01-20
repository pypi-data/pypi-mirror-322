from pyodm.model.definition import Attribute


class Length(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("Length")