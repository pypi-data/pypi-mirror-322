
import pyodm.model.meta.cdisc_odm_entity as Meta



from pyodm.model.definition import OneElement



class StateProv(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StateProv
    """

    def __init__(self):
        super().__init__()
        self.set_name("StateProv")
        

    