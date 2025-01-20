
import pyodm.model.meta.cdisc_odm_entity as Meta



from pyodm.model.definition import OneElement



class HouseNumber(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/HouseNumber
    """

    def __init__(self):
        super().__init__()
        self.set_name("HouseNumber")
        

    