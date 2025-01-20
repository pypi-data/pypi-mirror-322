
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.ArmOID import ArmOID

from pyodm.model.cdisc.classv2.attribute.EpochOID import EpochOID

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.WorkflowRef import WorkflowRef

from pyodm.model.cdisc.classv2.element.Coding import Coding

from pyodm.model.cdisc.classv2.element.StudyEventGroupRef import StudyEventGroupRef

from pyodm.model.cdisc.classv2.element.StudyEventRef import StudyEventRef


from pyodm.model.definition import ManyElements



class StudyEventGroupDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventGroupDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEventGroupDef")
        
        self._Description = None
        
        self._WorkflowRef = None
        
        self._Coding = None
        
        self._StudyEventGroupRef = None
        
        self._StudyEventRef = None
        
        self._OID = None
        
        self._Name = None
        
        self._ArmOID = None
        
        self._EpochOID = None
        
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
    def StudyEventGroupRef(self):
        """
        ManyElements
        """
        if self._StudyEventGroupRef is None:
            self._StudyEventGroupRef = StudyEventGroupRef()
        return self._StudyEventGroupRef
    
    @property
    def StudyEventRef(self):
        """
        OneElement
        """
        if self._StudyEventRef is None:
            self._StudyEventRef = StudyEventRef()
        return self._StudyEventRef
    
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
    def ArmOID(self):
        """
        Attribute
        """
        if self._ArmOID is None:
            self._ArmOID = ArmOID()
        return self._ArmOID
    
    @property
    def EpochOID(self):
        """
        Attribute
        """
        if self._EpochOID is None:
            self._EpochOID = EpochOID()
        return self._EpochOID
    
    @property
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    