
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.MethodSignature import MethodSignature

from pyodm.model.cdisc.classv2.element.FormalExpression import FormalExpression

from pyodm.model.cdisc.classv2.element.Alias import Alias

from pyodm.model.cdisc.classv2.element.DocumentRef import DocumentRef


from pyodm.model.definition import ManyElements



class MethodDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/MethodDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("MethodDef")
        
        self._Description = None
        
        self._MethodSignature = None
        
        self._FormalExpression = None
        
        self._Alias = None
        
        self._DocumentRef = None
        
        self._OID = None
        
        self._Name = None
        
        self._Type = None
        
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
    def MethodSignature(self):
        """
        ManyElements
        """
        if self._MethodSignature is None:
            self._MethodSignature = MethodSignature()
        return self._MethodSignature
    
    @property
    def FormalExpression(self):
        """
        ManyElements
        """
        if self._FormalExpression is None:
            self._FormalExpression = FormalExpression()
        return self._FormalExpression
    
    @property
    def Alias(self):
        """
        ManyElements
        """
        if self._Alias is None:
            self._Alias = Alias()
        return self._Alias
    
    @property
    def DocumentRef(self):
        """
        ManyElements
        """
        if self._DocumentRef is None:
            self._DocumentRef = DocumentRef()
        return self._DocumentRef
    
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
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    