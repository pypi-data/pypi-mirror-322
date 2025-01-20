
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Repeating import Repeating

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.Category import Category

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.ItemGroupRef import ItemGroupRef

from pyodm.model.cdisc.classv2.element.WorkflowRef import WorkflowRef

from pyodm.model.cdisc.classv2.element.Coding import Coding

from pyodm.model.cdisc.classv2.element.Alias import Alias


from pyodm.model.definition import ManyElements



class StudyEventDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEventDef")
        
        self._Description = None
        
        self._ItemGroupRef = None
        
        self._WorkflowRef = None
        
        self._Coding = None
        
        self._Alias = None
        
        self._OID = None
        
        self._Name = None
        
        self._Repeating = None
        
        self._Type = None
        
        self._Category = None
        
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
    def ItemGroupRef(self):
        """
        ManyElements
        """
        if self._ItemGroupRef is None:
            self._ItemGroupRef = ItemGroupRef()
        return self._ItemGroupRef
    
    @property
    def WorkflowRef(self):
        """
        ManyElements
        """
        if self._WorkflowRef is None:
            self._WorkflowRef = WorkflowRef()
        return self._WorkflowRef
    
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
    def Repeating(self):
        """
        Attribute
        """
        if self._Repeating is None:
            self._Repeating = Repeating()
        return self._Repeating
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def Category(self):
        """
        Attribute
        """
        if self._Category is None:
            self._Category = Category()
        return self._Category
    
    @property
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    