
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.InclusionCriteria import InclusionCriteria

from pyodm.model.cdisc.classv2.element.ExclusionCriteria import ExclusionCriteria


from pyodm.model.definition import OneElement



class InclusionExclusionCriteria(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/InclusionExclusionCriteria
    """

    def __init__(self):
        super().__init__()
        self.set_name("InclusionExclusionCriteria")
        
        self._InclusionCriteria = None
        
        self._ExclusionCriteria = None
        

    
    @property
    def InclusionCriteria(self):
        """
        OneElement
        """
        if self._InclusionCriteria is None:
            self._InclusionCriteria = InclusionCriteria()
        return self._InclusionCriteria
    
    @property
    def ExclusionCriteria(self):
        """
        OneElement
        """
        if self._ExclusionCriteria is None:
            self._ExclusionCriteria = ExclusionCriteria()
        return self._ExclusionCriteria
    