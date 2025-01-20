
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.FileType import FileType

from pyodm.model.cdisc.classv2.attribute.Granularity import Granularity

from pyodm.model.cdisc.classv2.attribute.Context import Context

from pyodm.model.cdisc.classv2.attribute.FileOID import FileOID

from pyodm.model.cdisc.classv2.attribute.CreationDateTime import CreationDateTime

from pyodm.model.cdisc.classv2.attribute.PriorFileOID import PriorFileOID

from pyodm.model.cdisc.classv2.attribute.AsOfDateTime import AsOfDateTime

from pyodm.model.cdisc.classv2.attribute.ODMVersion import ODMVersion

from pyodm.model.cdisc.classv2.attribute.Originator import Originator

from pyodm.model.cdisc.classv2.attribute.SourceSystem import SourceSystem

from pyodm.model.cdisc.classv2.attribute.SourceSystemVersion import SourceSystemVersion


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.Study import Study

from pyodm.model.cdisc.classv2.element.AdminData import AdminData

from pyodm.model.cdisc.classv2.element.ReferenceData import ReferenceData

from pyodm.model.cdisc.classv2.element.ClinicalData import ClinicalData

from pyodm.model.cdisc.classv2.element.Association import Association




class ODM(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ODM
    """

    def __init__(self):
        super().__init__()
        self.set_name("ODM")
        
        self._Description = None
        
        self._Study = None
        
        self._AdminData = None
        
        self._ReferenceData = None
        
        self._ClinicalData = None
        
        self._Association = None
        
        self._FileType = None
        
        self._Granularity = None
        
        self._Context = None
        
        self._FileOID = None
        
        self._CreationDateTime = None
        
        self._PriorFileOID = None
        
        self._AsOfDateTime = None
        
        self._ODMVersion = None
        
        self._Originator = None
        
        self._SourceSystem = None
        
        self._SourceSystemVersion = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def Study(self):
        """
        ManyElements
        """
        if self._Study is None:
            self._Study = Study()
        return self._Study
    
    @property
    def AdminData(self):
        """
        ManyElements
        """
        if self._AdminData is None:
            self._AdminData = AdminData()
        return self._AdminData
    
    @property
    def ReferenceData(self):
        """
        ManyElements
        """
        if self._ReferenceData is None:
            self._ReferenceData = ReferenceData()
        return self._ReferenceData
    
    @property
    def ClinicalData(self):
        """
        ManyElements
        """
        if self._ClinicalData is None:
            self._ClinicalData = ClinicalData()
        return self._ClinicalData
    
    @property
    def Association(self):
        """
        ManyElements
        """
        if self._Association is None:
            self._Association = Association()
        return self._Association
    
    @property
    def FileType(self):
        """
        Attribute
        """
        if self._FileType is None:
            self._FileType = FileType()
        return self._FileType
    
    @property
    def Granularity(self):
        """
        Attribute
        """
        if self._Granularity is None:
            self._Granularity = Granularity()
        return self._Granularity
    
    @property
    def Context(self):
        """
        Attribute
        """
        if self._Context is None:
            self._Context = Context()
        return self._Context
    
    @property
    def FileOID(self):
        """
        Attribute
        """
        if self._FileOID is None:
            self._FileOID = FileOID()
        return self._FileOID
    
    @property
    def CreationDateTime(self):
        """
        Attribute
        """
        if self._CreationDateTime is None:
            self._CreationDateTime = CreationDateTime()
        return self._CreationDateTime
    
    @property
    def PriorFileOID(self):
        """
        Attribute
        """
        if self._PriorFileOID is None:
            self._PriorFileOID = PriorFileOID()
        return self._PriorFileOID
    
    @property
    def AsOfDateTime(self):
        """
        Attribute
        """
        if self._AsOfDateTime is None:
            self._AsOfDateTime = AsOfDateTime()
        return self._AsOfDateTime
    
    @property
    def ODMVersion(self):
        """
        Attribute
        """
        if self._ODMVersion is None:
            self._ODMVersion = ODMVersion()
        return self._ODMVersion
    
    @property
    def Originator(self):
        """
        Attribute
        """
        if self._Originator is None:
            self._Originator = Originator()
        return self._Originator
    
    @property
    def SourceSystem(self):
        """
        Attribute
        """
        if self._SourceSystem is None:
            self._SourceSystem = SourceSystem()
        return self._SourceSystem
    
    @property
    def SourceSystemVersion(self):
        """
        Attribute
        """
        if self._SourceSystemVersion is None:
            self._SourceSystemVersion = SourceSystemVersion()
        return self._SourceSystemVersion
    