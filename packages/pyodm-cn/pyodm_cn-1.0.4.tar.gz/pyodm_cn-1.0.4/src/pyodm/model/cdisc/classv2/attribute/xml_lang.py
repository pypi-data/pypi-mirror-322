from pyodm.model.definition import Attribute


class XmlLang(Attribute):
    def __init__(self):
        super().__init__()
        self.set_name("xml_lang")