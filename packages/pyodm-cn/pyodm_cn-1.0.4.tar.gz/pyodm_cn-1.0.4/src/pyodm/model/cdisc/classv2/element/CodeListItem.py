
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.CodedValue import CodedValue

from pyodm.model.cdisc.classv2.attribute.Rank import Rank

from pyodm.model.cdisc.classv2.attribute.Other import Other

from pyodm.model.cdisc.classv2.attribute.OrderNumber import OrderNumber

from pyodm.model.cdisc.classv2.attribute.ExtendedValue import ExtendedValue

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.Decode import Decode

from pyodm.model.cdisc.classv2.element.Coding import Coding

from pyodm.model.cdisc.classv2.element.Alias import Alias


from pyodm.model.definition import ManyElements



class CodeListItem(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/CodeListItem
    """

    def __init__(self):
        super().__init__()
        self.set_name("CodeListItem")
        
        self._Description = None
        
        self._Decode = None
        
        self._Coding = None
        
        self._Alias = None
        
        self._CodedValue = None
        
        self._Rank = None
        
        self._Other = None
        
        self._OrderNumber = None
        
        self._ExtendedValue = None
        
        self._CommentOID = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def Decode(self):
        """
        OneElement
        """
        if self._Decode is None:
            self._Decode = Decode()
        return self._Decode
    
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
    def CodedValue(self):
        """
        Attribute
        """
        if self._CodedValue is None:
            self._CodedValue = CodedValue()
        return self._CodedValue
    
    @property
    def Rank(self):
        """
        Attribute
        """
        if self._Rank is None:
            self._Rank = Rank()
        return self._Rank
    
    @property
    def Other(self):
        """
        Attribute
        """
        if self._Other is None:
            self._Other = Other()
        return self._Other
    
    @property
    def OrderNumber(self):
        """
        Attribute
        """
        if self._OrderNumber is None:
            self._OrderNumber = OrderNumber()
        return self._OrderNumber
    
    @property
    def ExtendedValue(self):
        """
        Attribute
        """
        if self._ExtendedValue is None:
            self._ExtendedValue = ExtendedValue()
        return self._ExtendedValue
    
    @property
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    