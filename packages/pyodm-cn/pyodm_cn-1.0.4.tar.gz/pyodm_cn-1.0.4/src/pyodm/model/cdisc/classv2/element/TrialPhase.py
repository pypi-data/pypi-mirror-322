
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Value import Value


from pyodm.model.cdisc.classv2.element.Description import Description


from pyodm.model.definition import OneElement



class TrialPhase(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/TrialPhase
    """

    def __init__(self):
        super().__init__()
        self.set_name("TrialPhase")
        
        self._Description = None
        
        self._Value = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def Value(self):
        """
        Attribute
        """
        if self._Value is None:
            self._Value = Value()
        return self._Value
    