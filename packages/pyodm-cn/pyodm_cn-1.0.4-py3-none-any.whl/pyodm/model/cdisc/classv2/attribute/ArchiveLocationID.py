from pyodm.model.definition import Attribute


class ArchiveLocationID(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("ArchiveLocationID")