
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.EndOID import EndOID



from pyodm.model.definition import ManyElements



class WorkflowEnd(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/WorkflowEnd
    """

    def __init__(self):
        super().__init__()
        self.set_name("WorkflowEnd")
        
        self._EndOID = None
        

    
    @property
    def EndOID(self):
        """
        Attribute
        """
        if self._EndOID is None:
            self._EndOID = EndOID()
        return self._EndOID
    