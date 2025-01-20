from pyodm.model.definition import Attribute


class TransitionOID(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("TransitionOID")