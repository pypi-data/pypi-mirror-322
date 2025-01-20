
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Repeating import Repeating

from pyodm.model.cdisc.classv2.attribute.RepeatingLimit import RepeatingLimit

from pyodm.model.cdisc.classv2.attribute.IsReferenceData import IsReferenceData

from pyodm.model.cdisc.classv2.attribute.Structure import Structure

from pyodm.model.cdisc.classv2.attribute.ArchiveLocationID import ArchiveLocationID

from pyodm.model.cdisc.classv2.attribute.DatasetName import DatasetName

from pyodm.model.cdisc.classv2.attribute.Domain import Domain

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.Purpose import Purpose

from pyodm.model.cdisc.classv2.attribute.StandardOID import StandardOID

from pyodm.model.cdisc.classv2.attribute.IsNonStandard import IsNonStandard

from pyodm.model.cdisc.classv2.attribute.HasNoData import HasNoData

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.Class import Class

from pyodm.model.cdisc.classv2.element.Coding import Coding

from pyodm.model.cdisc.classv2.element.WorkflowRef import WorkflowRef

from pyodm.model.cdisc.classv2.element.Origin import Origin

from pyodm.model.cdisc.classv2.element.Alias import Alias

from pyodm.model.cdisc.classv2.element.Leaf import Leaf

from pyodm.model.cdisc.classv2.element.ItemGroupRef import ItemGroupRef

from pyodm.model.cdisc.classv2.element.ItemRef import ItemRef


from pyodm.model.definition import ManyElements



class ItemGroupDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemGroupDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("ItemGroupDef")
        
        self._Description = None
        
        self._Class = None
        
        self._Coding = None
        
        self._WorkflowRef = None
        
        self._Origin = None
        
        self._Alias = None
        
        self._Leaf = None
        
        self._ItemGroupRef = None
        
        self._ItemRef = None
        
        self._OID = None
        
        self._Name = None
        
        self._Repeating = None
        
        self._RepeatingLimit = None
        
        self._IsReferenceData = None
        
        self._Structure = None
        
        self._ArchiveLocationID = None
        
        self._DatasetName = None
        
        self._Domain = None
        
        self._Type = None
        
        self._Purpose = None
        
        self._StandardOID = None
        
        self._IsNonStandard = None
        
        self._HasNoData = None
        
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
    def Class(self):
        """
        ManyElements
        """
        if self._Class is None:
            self._Class = Class()
        return self._Class
    
    @property
    def Coding(self):
        """
        ManyElements
        """
        if self._Coding is None:
            self._Coding = Coding()
        return self._Coding
    
    @property
    def WorkflowRef(self):
        """
        ManyElements
        """
        if self._WorkflowRef is None:
            self._WorkflowRef = WorkflowRef()
        return self._WorkflowRef
    
    @property
    def Origin(self):
        """
        ManyElements
        """
        if self._Origin is None:
            self._Origin = Origin()
        return self._Origin
    
    @property
    def Alias(self):
        """
        ManyElements
        """
        if self._Alias is None:
            self._Alias = Alias()
        return self._Alias
    
    @property
    def Leaf(self):
        """
        ManyElements
        """
        if self._Leaf is None:
            self._Leaf = Leaf()
        return self._Leaf
    
    @property
    def ItemGroupRef(self):
        """
        ManyElements
        """
        if self._ItemGroupRef is None:
            self._ItemGroupRef = ItemGroupRef()
        return self._ItemGroupRef
    
    @property
    def ItemRef(self):
        """
        ManyElements
        """
        if self._ItemRef is None:
            self._ItemRef = ItemRef()
        return self._ItemRef
    
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
    def RepeatingLimit(self):
        """
        Attribute
        """
        if self._RepeatingLimit is None:
            self._RepeatingLimit = RepeatingLimit()
        return self._RepeatingLimit
    
    @property
    def IsReferenceData(self):
        """
        Attribute
        """
        if self._IsReferenceData is None:
            self._IsReferenceData = IsReferenceData()
        return self._IsReferenceData
    
    @property
    def Structure(self):
        """
        Attribute
        """
        if self._Structure is None:
            self._Structure = Structure()
        return self._Structure
    
    @property
    def ArchiveLocationID(self):
        """
        Attribute
        """
        if self._ArchiveLocationID is None:
            self._ArchiveLocationID = ArchiveLocationID()
        return self._ArchiveLocationID
    
    @property
    def DatasetName(self):
        """
        Attribute
        """
        if self._DatasetName is None:
            self._DatasetName = DatasetName()
        return self._DatasetName
    
    @property
    def Domain(self):
        """
        Attribute
        """
        if self._Domain is None:
            self._Domain = Domain()
        return self._Domain
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def Purpose(self):
        """
        Attribute
        """
        if self._Purpose is None:
            self._Purpose = Purpose()
        return self._Purpose
    
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
    
    @property
    def HasNoData(self):
        """
        Attribute
        """
        if self._HasNoData is None:
            self._HasNoData = HasNoData()
        return self._HasNoData
    
    @property
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    