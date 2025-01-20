
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Context import Context



from pyodm.model.definition import ManyElements



class FormalExpression(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/FormalExpression
    """

    def __init__(self):
        super().__init__()
        self.set_name("FormalExpression")
        
        self._Context = None
        

    
    @property
    def Context(self):
        """
        Attribute
        """
        if self._Context is None:
            self._Context = Context()
        return self._Context
    