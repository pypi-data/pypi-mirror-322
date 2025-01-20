
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Term import Term

from pyodm.model.cdisc.classv2.attribute.ShortName import ShortName


from pyodm.model.cdisc.classv2.element.ParameterValue import ParameterValue

from pyodm.model.cdisc.classv2.element.Coding import Coding


from pyodm.model.definition import ManyElements



class StudyParameter(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyParameter
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyParameter")
        
        self._ParameterValue = None
        
        self._Coding = None
        
        self._OID = None
        
        self._Term = None
        
        self._ShortName = None
        

    
    @property
    def ParameterValue(self):
        """
        ManyElements
        """
        if self._ParameterValue is None:
            self._ParameterValue = ParameterValue()
        return self._ParameterValue
    
    @property
    def Coding(self):
        """
        ManyElements
        """
        if self._Coding is None:
            self._Coding = Coding()
        return self._Coding
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    
    @property
    def Term(self):
        """
        Attribute
        """
        if self._Term is None:
            self._Term = Term()
        return self._Term
    
    @property
    def ShortName(self):
        """
        Attribute
        """
        if self._ShortName is None:
            self._ShortName = ShortName()
        return self._ShortName
    