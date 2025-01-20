
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyEventOID import StudyEventOID

from pyodm.model.cdisc.classv2.attribute.StudyEventRepeatKey import StudyEventRepeatKey

from pyodm.model.cdisc.classv2.attribute.TransactionType import TransactionType


from pyodm.model.cdisc.classv2.element.ItemGroupData import ItemGroupData

from pyodm.model.cdisc.classv2.element.Query import Query

from pyodm.model.cdisc.classv2.element.AuditRecord import AuditRecord

from pyodm.model.cdisc.classv2.element.Signature import Signature

from pyodm.model.cdisc.classv2.element.Annotation import Annotation


from pyodm.model.definition import ManyElements



class StudyEventData(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventData
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEventData")
        
        self._ItemGroupData = None
        
        self._Query = None
        
        self._AuditRecord = None
        
        self._Signature = None
        
        self._Annotation = None
        
        self._StudyEventOID = None
        
        self._StudyEventRepeatKey = None
        
        self._TransactionType = None
        

    
    @property
    def ItemGroupData(self):
        """
        ManyElements
        """
        if self._ItemGroupData is None:
            self._ItemGroupData = ItemGroupData()
        return self._ItemGroupData
    
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
    def StudyEventOID(self):
        """
        Attribute
        """
        if self._StudyEventOID is None:
            self._StudyEventOID = StudyEventOID()
        return self._StudyEventOID
    
    @property
    def StudyEventRepeatKey(self):
        """
        Attribute
        """
        if self._StudyEventRepeatKey is None:
            self._StudyEventRepeatKey = StudyEventRepeatKey()
        return self._StudyEventRepeatKey
    
    @property
    def TransactionType(self):
        """
        Attribute
        """
        if self._TransactionType is None:
            self._TransactionType = TransactionType()
        return self._TransactionType
    