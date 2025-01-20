from pyodm.model.definition import Attribute


class Term(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("Term")