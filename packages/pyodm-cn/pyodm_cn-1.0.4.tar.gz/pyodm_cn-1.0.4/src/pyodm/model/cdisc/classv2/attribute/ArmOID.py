from pyodm.model.definition import Attribute


class ArmOID(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("ArmOID")