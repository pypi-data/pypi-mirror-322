
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.Criterion import Criterion


from pyodm.model.definition import OneElement



class ExclusionCriteria(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ExclusionCriteria
    """

    def __init__(self):
        super().__init__()
        self.set_name("ExclusionCriteria")
        
        self._Criterion = None
        

    
    @property
    def Criterion(self):
        """
        ManyElements
        """
        if self._Criterion is None:
            self._Criterion = Criterion()
        return self._Criterion
    