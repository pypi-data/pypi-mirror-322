
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StartOID import StartOID



from pyodm.model.definition import OneElement



class WorkflowStart(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/WorkflowStart
    """

    def __init__(self):
        super().__init__()
        self.set_name("WorkflowStart")
        
        self._StartOID = None
        

    
    @property
    def StartOID(self):
        """
        Attribute
        """
        if self._StartOID is None:
            self._StartOID = StartOID()
        return self._StartOID
    