
import pyodm.model.meta.cdisc_odm_entity as Meta





class CheckValue(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/CheckValue
    """

    def __init__(self):
        super().__init__()
        self.set_name("CheckValue")
        

    