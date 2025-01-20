
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Context import Context

from pyodm.model.cdisc.classv2.attribute.Name import Name



from pyodm.model.definition import ManyElements



class Alias(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Alias
    """

    def __init__(self):
        super().__init__()
        self.set_name("Alias")
        
        self._Context = None
        
        self._Name = None
        

    
    @property
    def Context(self):
        """
        Attribute
        """
        if self._Context is None:
            self._Context = Context()
        return self._Context
    
    @property
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    