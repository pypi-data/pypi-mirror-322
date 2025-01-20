
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.FlagValue import FlagValue

from pyodm.model.cdisc.classv2.element.FlagType import FlagType


from pyodm.model.definition import ManyElements



class Flag(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Flag
    """

    def __init__(self):
        super().__init__()
        self.set_name("Flag")
        
        self._FlagValue = None
        
        self._FlagType = None
        

    
    @property
    def FlagValue(self):
        """
        OneElement
        """
        if self._FlagValue is None:
            self._FlagValue = FlagValue()
        return self._FlagValue
    
    @property
    def FlagType(self):
        """
        OneElement
        """
        if self._FlagType is None:
            self._FlagType = FlagType()
        return self._FlagType
    