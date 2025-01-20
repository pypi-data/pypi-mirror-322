from pyodm.model.definition import Attribute


class XlinkHref(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("xlink_href")