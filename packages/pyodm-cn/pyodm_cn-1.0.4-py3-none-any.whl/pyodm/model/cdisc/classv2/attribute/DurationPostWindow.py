from pyodm.model.definition import Attribute


class DurationPostWindow(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("DurationPostWindow")