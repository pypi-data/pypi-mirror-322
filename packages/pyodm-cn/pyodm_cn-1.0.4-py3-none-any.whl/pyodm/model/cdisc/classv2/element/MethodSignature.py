
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.Parameter import Parameter

from pyodm.model.cdisc.classv2.element.ReturnValue import ReturnValue


from pyodm.model.definition import ManyElements



class MethodSignature(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/MethodSignature
    """

    def __init__(self):
        super().__init__()
        self.set_name("MethodSignature")
        
        self._Parameter = None
        
        self._ReturnValue = None
        

    
    @property
    def Parameter(self):
        """
        ManyElements
        """
        if self._Parameter is None:
            self._Parameter = Parameter()
        return self._Parameter
    
    @property
    def ReturnValue(self):
        """
        ManyElements
        """
        if self._ReturnValue is None:
            self._ReturnValue = ReturnValue()
        return self._ReturnValue
    