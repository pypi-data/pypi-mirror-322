
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.ValueListOID import ValueListOID



from pyodm.model.definition import ManyElements



class ValueListRef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ValueListRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("ValueListRef")
        
        self._ValueListOID = None
        

    
    @property
    def ValueListOID(self):
        """
        Attribute
        """
        if self._ValueListOID is None:
            self._ValueListOID = ValueListOID()
        return self._ValueListOID
    