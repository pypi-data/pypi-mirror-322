from pyodm.model.definition import Attribute


class ItemGroupOID(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("ItemGroupOID")