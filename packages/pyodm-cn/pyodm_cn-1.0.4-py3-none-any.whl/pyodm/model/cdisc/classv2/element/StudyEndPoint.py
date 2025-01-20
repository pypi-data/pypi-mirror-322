
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.Level import Level


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.FormalExpression import FormalExpression


from pyodm.model.definition import ManyElements



class StudyEndPoint(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEndPoint
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEndPoint")
        
        self._Description = None
        
        self._FormalExpression = None
        
        self._OID = None
        
        self._Name = None
        
        self._Type = None
        
        self._Level = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
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
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def Level(self):
        """
        Attribute
        """
        if self._Level is None:
            self._Level = Level()
        return self._Level
    