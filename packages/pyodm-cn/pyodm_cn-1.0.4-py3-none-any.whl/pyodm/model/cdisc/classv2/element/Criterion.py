
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.ConditionOID import ConditionOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.Coding import Coding


from pyodm.model.definition import ManyElements



class Criterion(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Criterion
    """

    def __init__(self):
        super().__init__()
        self.set_name("Criterion")
        
        self._Description = None
        
        self._Coding = None
        
        self._OID = None
        
        self._Name = None
        
        self._ConditionOID = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
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
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    
    @property
    def ConditionOID(self):
        """
        Attribute
        """
        if self._ConditionOID is None:
            self._ConditionOID = ConditionOID()
        return self._ConditionOID
    