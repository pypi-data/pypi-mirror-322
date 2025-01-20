from pyodm.model.definition import Attribute


class SystemName(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("SystemName")