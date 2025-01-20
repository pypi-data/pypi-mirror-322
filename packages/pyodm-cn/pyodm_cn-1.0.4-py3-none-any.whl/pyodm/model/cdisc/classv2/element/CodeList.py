
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.DataType import DataType

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID

from pyodm.model.cdisc.classv2.attribute.StandardOID import StandardOID

from pyodm.model.cdisc.classv2.attribute.IsNonStandard import IsNonStandard


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.CodeListItem import CodeListItem

from pyodm.model.cdisc.classv2.element.Coding import Coding

from pyodm.model.cdisc.classv2.element.Alias import Alias


from pyodm.model.definition import ManyElements



class CodeList(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/CodeList
    """

    def __init__(self):
        super().__init__()
        self.set_name("CodeList")
        
        self._Description = None
        
        self._CodeListItem = None
        
        self._Coding = None
        
        self._Alias = None
        
        self._OID = None
        
        self._Name = None
        
        self._DataType = None
        
        self._CommentOID = None
        
        self._StandardOID = None
        
        self._IsNonStandard = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def CodeListItem(self):
        """
        ManyElements
        """
        if self._CodeListItem is None:
            self._CodeListItem = CodeListItem()
        return self._CodeListItem
    
    @property
    def Coding(self):
        """
        ManyElements
        """
        if self._Coding is None:
            self._Coding = Coding()
        return self._Coding
    
    @property
    def Alias(self):
        """
        ManyElements
        """
        if self._Alias is None:
            self._Alias = Alias()
        return self._Alias
    
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
    def DataType(self):
        """
        Attribute
        """
        if self._DataType is None:
            self._DataType = DataType()
        return self._DataType
    
    @property
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    
    @property
    def StandardOID(self):
        """
        Attribute
        """
        if self._StandardOID is None:
            self._StandardOID = StandardOID()
        return self._StandardOID
    
    @property
    def IsNonStandard(self):
        """
        Attribute
        """
        if self._IsNonStandard is None:
            self._IsNonStandard = IsNonStandard()
        return self._IsNonStandard
    