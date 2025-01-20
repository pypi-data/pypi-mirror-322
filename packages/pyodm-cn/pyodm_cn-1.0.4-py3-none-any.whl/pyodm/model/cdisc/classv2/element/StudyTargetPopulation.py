
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.Coding import Coding

from pyodm.model.cdisc.classv2.element.FormalExpression import FormalExpression


from pyodm.model.definition import OneElement



class StudyTargetPopulation(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTargetPopulation
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyTargetPopulation")
        
        self._Description = None
        
        self._Coding = None
        
        self._FormalExpression = None
        
        self._OID = None
        
        self._Name = None
        

    
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
    def FormalExpression(self):
        """
        ManyElements
        """
        if self._FormalExpression is None:
            self._FormalExpression = FormalExpression()
        return self._FormalExpression
    
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
    