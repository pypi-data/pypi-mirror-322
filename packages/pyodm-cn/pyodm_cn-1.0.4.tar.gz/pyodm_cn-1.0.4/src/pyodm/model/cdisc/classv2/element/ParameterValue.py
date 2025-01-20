
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Value import Value


from pyodm.model.cdisc.classv2.element.Coding import Coding


from pyodm.model.definition import ManyElements



class ParameterValue(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ParameterValue
    """

    def __init__(self):
        super().__init__()
        self.set_name("ParameterValue")
        
        self._Coding = None
        
        self._Value = None
        

    
    @property
    def Coding(self):
        """
        ManyElements
        """
        if self._Coding is None:
            self._Coding = Coding()
        return self._Coding
    
    @property
    def Value(self):
        """
        Attribute
        """
        if self._Value is None:
            self._Value = Value()
        return self._Value
    