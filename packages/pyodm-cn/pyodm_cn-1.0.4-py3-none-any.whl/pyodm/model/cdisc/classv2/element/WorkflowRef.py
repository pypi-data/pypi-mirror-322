
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.WorkflowOID import WorkflowOID



from pyodm.model.definition import ManyElements



class WorkflowRef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/WorkflowRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("WorkflowRef")
        
        self._WorkflowOID = None
        

    
    @property
    def WorkflowOID(self):
        """
        Attribute
        """
        if self._WorkflowOID is None:
            self._WorkflowOID = WorkflowOID()
        return self._WorkflowOID
    