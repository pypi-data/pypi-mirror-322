
import pyodm.model.meta.cdisc_odm_entity as Meta



from pyodm.model.definition import ManyElements



class SubClass(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SubClass
    """

    def __init__(self):
        super().__init__()
        self.set_name("SubClass")
        

    