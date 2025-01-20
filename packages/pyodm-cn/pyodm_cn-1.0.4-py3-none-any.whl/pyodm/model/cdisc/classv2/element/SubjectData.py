
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.SubjectKey import SubjectKey

from pyodm.model.cdisc.classv2.attribute.TransactionType import TransactionType


from pyodm.model.cdisc.classv2.element.InvestigatorRef import InvestigatorRef

from pyodm.model.cdisc.classv2.element.SiteRef import SiteRef

from pyodm.model.cdisc.classv2.element.StudyEventData import StudyEventData

from pyodm.model.cdisc.classv2.element.Query import Query

from pyodm.model.cdisc.classv2.element.AuditRecord import AuditRecord

from pyodm.model.cdisc.classv2.element.Signature import Signature

from pyodm.model.cdisc.classv2.element.Annotation import Annotation


from pyodm.model.definition import ManyElements



class SubjectData(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SubjectData
    """

    def __init__(self):
        super().__init__()
        self.set_name("SubjectData")
        
        self._InvestigatorRef = None
        
        self._SiteRef = None
        
        self._StudyEventData = None
        
        self._Query = None
        
        self._AuditRecord = None
        
        self._Signature = None
        
        self._Annotation = None
        
        self._SubjectKey = None
        
        self._TransactionType = None
        

    
    @property
    def InvestigatorRef(self):
        """
        OneElement
        """
        if self._InvestigatorRef is None:
            self._InvestigatorRef = InvestigatorRef()
        return self._InvestigatorRef
    
    @property
    def SiteRef(self):
        """
        OneElement
        """
        if self._SiteRef is None:
            self._SiteRef = SiteRef()
        return self._SiteRef
    
    @property
    def StudyEventData(self):
        """
        ManyElements
        """
        if self._StudyEventData is None:
            self._StudyEventData = StudyEventData()
        return self._StudyEventData
    
    @property
    def Query(self):
        """
        ManyElements
        """
        if self._Query is None:
            self._Query = Query()
        return self._Query
    
    @property
    def AuditRecord(self):
        """
        ManyElements
        """
        if self._AuditRecord is None:
            self._AuditRecord = AuditRecord()
        return self._AuditRecord
    
    @property
    def Signature(self):
        """
        OneElement
        """
        if self._Signature is None:
            self._Signature = Signature()
        return self._Signature
    
    @property
    def Annotation(self):
        """
        ManyElements
        """
        if self._Annotation is None:
            self._Annotation = Annotation()
        return self._Annotation
    
    @property
    def SubjectKey(self):
        """
        Attribute
        """
        if self._SubjectKey is None:
            self._SubjectKey = SubjectKey()
        return self._SubjectKey
    
    @property
    def TransactionType(self):
        """
        Attribute
        """
        if self._TransactionType is None:
            self._TransactionType = TransactionType()
        return self._TransactionType
    