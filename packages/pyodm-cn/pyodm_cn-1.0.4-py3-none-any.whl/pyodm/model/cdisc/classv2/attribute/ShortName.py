from pyodm.model.definition import Attribute


class ShortName(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("ShortName")