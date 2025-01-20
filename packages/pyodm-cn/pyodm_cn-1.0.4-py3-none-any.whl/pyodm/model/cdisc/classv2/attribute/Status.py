from pyodm.model.definition import Attribute


class Status(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("Status")