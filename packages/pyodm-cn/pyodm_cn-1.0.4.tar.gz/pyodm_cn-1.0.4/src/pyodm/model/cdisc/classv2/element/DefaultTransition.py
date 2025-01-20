
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.TargetTransitionOID import TargetTransitionOID



from pyodm.model.definition import ManyElements



class DefaultTransition(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/DefaultTransition
    """

    def __init__(self):
        super().__init__()
        self.set_name("DefaultTransition")
        
        self._TargetTransitionOID = None
        

    
    @property
    def TargetTransitionOID(self):
        """
        Attribute
        """
        if self._TargetTransitionOID is None:
            self._TargetTransitionOID = TargetTransitionOID()
        return self._TargetTransitionOID
    