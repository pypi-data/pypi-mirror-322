
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.CodeListOID import CodeListOID



from pyodm.model.definition import OneElement



class FlagType(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/FlagType
    """

    def __init__(self):
        super().__init__()
        self.set_name("FlagType")
        
        self._CodeListOID = None
        

    
    @property
    def CodeListOID(self):
        """
        Attribute
        """
        if self._CodeListOID is None:
            self._CodeListOID = CodeListOID()
        return self._CodeListOID
    