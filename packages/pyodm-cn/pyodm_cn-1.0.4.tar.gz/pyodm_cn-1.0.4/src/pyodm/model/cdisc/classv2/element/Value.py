
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.SeqNum import SeqNum



from pyodm.model.definition import ManyElements



class Value(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Value
    """

    def __init__(self):
        super().__init__()
        self.set_name("Value")
        
        self._SeqNum = None
        

    
    @property
    def SeqNum(self):
        """
        Attribute
        """
        if self._SeqNum is None:
            self._SeqNum = SeqNum()
        return self._SeqNum
    