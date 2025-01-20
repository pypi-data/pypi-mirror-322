
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.TargetTransitionOID import TargetTransitionOID

from pyodm.model.cdisc.classv2.attribute.ConditionOID import ConditionOID



from pyodm.model.definition import ManyElements



class TargetTransition(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/TargetTransition
    """

    def __init__(self):
        super().__init__()
        self.set_name("TargetTransition")
        
        self._TargetTransitionOID = None
        
        self._ConditionOID = None
        

    
    @property
    def TargetTransitionOID(self):
        """
        Attribute
        """
        if self._TargetTransitionOID is None:
            self._TargetTransitionOID = TargetTransitionOID()
        return self._TargetTransitionOID
    
    @property
    def ConditionOID(self):
        """
        Attribute
        """
        if self._ConditionOID is None:
            self._ConditionOID = ConditionOID()
        return self._ConditionOID
    