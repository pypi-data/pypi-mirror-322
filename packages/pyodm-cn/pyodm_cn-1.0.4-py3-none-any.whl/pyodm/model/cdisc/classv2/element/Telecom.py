
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.TelecomType import TelecomType

from pyodm.model.cdisc.classv2.attribute.Value import Value



from pyodm.model.definition import ManyElements



class Telecom(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Telecom
    """

    def __init__(self):
        super().__init__()
        self.set_name("Telecom")
        
        self._TelecomType = None
        
        self._Value = None
        

    
    @property
    def TelecomType(self):
        """
        Attribute
        """
        if self._TelecomType is None:
            self._TelecomType = TelecomType()
        return self._TelecomType
    
    @property
    def Value(self):
        """
        Attribute
        """
        if self._Value is None:
            self._Value = Value()
        return self._Value
    