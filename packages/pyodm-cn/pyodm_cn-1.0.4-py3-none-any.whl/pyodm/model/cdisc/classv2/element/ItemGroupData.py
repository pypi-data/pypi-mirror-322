
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.ItemGroupOID import ItemGroupOID

from pyodm.model.cdisc.classv2.attribute.ItemGroupRepeatKey import ItemGroupRepeatKey

from pyodm.model.cdisc.classv2.attribute.TransactionType import TransactionType

from pyodm.model.cdisc.classv2.attribute.ItemGroupDataSeq import ItemGroupDataSeq


from pyodm.model.cdisc.classv2.element.Query import Query

from pyodm.model.cdisc.classv2.element.ItemData import ItemData

from pyodm.model.cdisc.classv2.element.AuditRecord import AuditRecord

from pyodm.model.cdisc.classv2.element.Signature import Signature

from pyodm.model.cdisc.classv2.element.Annotation import Annotation


from pyodm.model.definition import ManyElements



class ItemGroupData(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemGroupData
    """

    def __init__(self):
        super().__init__()
        self.set_name("ItemGroupData")
        
        self._Query = None
        
        self._ItemGroupData = None
        
        self._ItemData = None
        
        self._AuditRecord = None
        
        self._Signature = None
        
        self._Annotation = None
        
        self._ItemGroupOID = None
        
        self._ItemGroupRepeatKey = None
        
        self._TransactionType = None
        
        self._ItemGroupDataSeq = None
        

    
    @property
    def Query(self):
        """
        ManyElements
        """
        if self._Query is None:
            self._Query = Query()
        return self._Query
    
    @property
    def ItemGroupData(self):
        """
        ManyElements
        """
        if self._ItemGroupData is None:
            self._ItemGroupData = ItemGroupData()
        return self._ItemGroupData
    
    @property
    def ItemData(self):
        """
        ManyElements
        """
        if self._ItemData is None:
            self._ItemData = ItemData()
        return self._ItemData
    
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
    def ItemGroupOID(self):
        """
        Attribute
        """
        if self._ItemGroupOID is None:
            self._ItemGroupOID = ItemGroupOID()
        return self._ItemGroupOID
    
    @property
    def ItemGroupRepeatKey(self):
        """
        Attribute
        """
        if self._ItemGroupRepeatKey is None:
            self._ItemGroupRepeatKey = ItemGroupRepeatKey()
        return self._ItemGroupRepeatKey
    
    @property
    def TransactionType(self):
        """
        Attribute
        """
        if self._TransactionType is None:
            self._TransactionType = TransactionType()
        return self._TransactionType
    
    @property
    def ItemGroupDataSeq(self):
        """
        Attribute
        """
        if self._ItemGroupDataSeq is None:
            self._ItemGroupDataSeq = ItemGroupDataSeq()
        return self._ItemGroupDataSeq
    