
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.Include import Include

from pyodm.model.cdisc.classv2.element.Standards import Standards

from pyodm.model.cdisc.classv2.element.AnnotatedCRF import AnnotatedCRF

from pyodm.model.cdisc.classv2.element.SupplementalDoc import SupplementalDoc

from pyodm.model.cdisc.classv2.element.ValueListDef import ValueListDef

from pyodm.model.cdisc.classv2.element.WhereClauseDef import WhereClauseDef

from pyodm.model.cdisc.classv2.element.Protocol import Protocol

from pyodm.model.cdisc.classv2.element.WorkflowDef import WorkflowDef

from pyodm.model.cdisc.classv2.element.StudyEventGroupDef import StudyEventGroupDef

from pyodm.model.cdisc.classv2.element.StudyEventDef import StudyEventDef

from pyodm.model.cdisc.classv2.element.ItemGroupDef import ItemGroupDef

from pyodm.model.cdisc.classv2.element.ItemDef import ItemDef

from pyodm.model.cdisc.classv2.element.CodeList import CodeList

from pyodm.model.cdisc.classv2.element.ConditionDef import ConditionDef

from pyodm.model.cdisc.classv2.element.MethodDef import MethodDef

from pyodm.model.cdisc.classv2.element.CommentDef import CommentDef

from pyodm.model.cdisc.classv2.element.Leaf import Leaf


from pyodm.model.definition import ManyElements



class MetaDataVersion(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/MetaDataVersion
    """

    def __init__(self):
        super().__init__()
        self.set_name("MetaDataVersion")
        
        self._Description = None
        
        self._Include = None
        
        self._Standards = None
        
        self._AnnotatedCRF = None
        
        self._SupplementalDoc = None
        
        self._ValueListDef = None
        
        self._WhereClauseDef = None
        
        self._Protocol = None
        
        self._WorkflowDef = None
        
        self._StudyEventGroupDef = None
        
        self._StudyEventDef = None
        
        self._ItemGroupDef = None
        
        self._ItemDef = None
        
        self._CodeList = None
        
        self._ConditionDef = None
        
        self._MethodDef = None
        
        self._CommentDef = None
        
        self._Leaf = None
        
        self._OID = None
        
        self._Name = None
        
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
    def Include(self):
        """
        ManyElements
        """
        if self._Include is None:
            self._Include = Include()
        return self._Include
    
    @property
    def Standards(self):
        """
        ManyElements
        """
        if self._Standards is None:
            self._Standards = Standards()
        return self._Standards
    
    @property
    def AnnotatedCRF(self):
        """
        ManyElements
        """
        if self._AnnotatedCRF is None:
            self._AnnotatedCRF = AnnotatedCRF()
        return self._AnnotatedCRF
    
    @property
    def SupplementalDoc(self):
        """
        ManyElements
        """
        if self._SupplementalDoc is None:
            self._SupplementalDoc = SupplementalDoc()
        return self._SupplementalDoc
    
    @property
    def ValueListDef(self):
        """
        ManyElements
        """
        if self._ValueListDef is None:
            self._ValueListDef = ValueListDef()
        return self._ValueListDef
    
    @property
    def WhereClauseDef(self):
        """
        ManyElements
        """
        if self._WhereClauseDef is None:
            self._WhereClauseDef = WhereClauseDef()
        return self._WhereClauseDef
    
    @property
    def Protocol(self):
        """
        ManyElements
        """
        if self._Protocol is None:
            self._Protocol = Protocol()
        return self._Protocol
    
    @property
    def WorkflowDef(self):
        """
        ManyElements
        """
        if self._WorkflowDef is None:
            self._WorkflowDef = WorkflowDef()
        return self._WorkflowDef
    
    @property
    def StudyEventGroupDef(self):
        """
        ManyElements
        """
        if self._StudyEventGroupDef is None:
            self._StudyEventGroupDef = StudyEventGroupDef()
        return self._StudyEventGroupDef
    
    @property
    def StudyEventDef(self):
        """
        ManyElements
        """
        if self._StudyEventDef is None:
            self._StudyEventDef = StudyEventDef()
        return self._StudyEventDef
    
    @property
    def ItemGroupDef(self):
        """
        ManyElements
        """
        if self._ItemGroupDef is None:
            self._ItemGroupDef = ItemGroupDef()
        return self._ItemGroupDef
    
    @property
    def ItemDef(self):
        """
        ManyElements
        """
        if self._ItemDef is None:
            self._ItemDef = ItemDef()
        return self._ItemDef
    
    @property
    def CodeList(self):
        """
        ManyElements
        """
        if self._CodeList is None:
            self._CodeList = CodeList()
        return self._CodeList
    
    @property
    def ConditionDef(self):
        """
        ManyElements
        """
        if self._ConditionDef is None:
            self._ConditionDef = ConditionDef()
        return self._ConditionDef
    
    @property
    def MethodDef(self):
        """
        ManyElements
        """
        if self._MethodDef is None:
            self._MethodDef = MethodDef()
        return self._MethodDef
    
    @property
    def CommentDef(self):
        """
        ManyElements
        """
        if self._CommentDef is None:
            self._CommentDef = CommentDef()
        return self._CommentDef
    
    @property
    def Leaf(self):
        """
        ManyElements
        """
        if self._Leaf is None:
            self._Leaf = Leaf()
        return self._Leaf
    
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
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    