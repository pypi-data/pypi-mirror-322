
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.ItemOID import ItemOID

from pyodm.model.cdisc.classv2.attribute.TransactionType import TransactionType

from pyodm.model.cdisc.classv2.attribute.IsNull import IsNull


from pyodm.model.cdisc.classv2.element.Value import Value

from pyodm.model.cdisc.classv2.element.Query import Query

from pyodm.model.cdisc.classv2.element.AuditRecord import AuditRecord

from pyodm.model.cdisc.classv2.element.Signature import Signature

from pyodm.model.cdisc.classv2.element.Annotation import Annotation


from pyodm.model.definition import ManyElements



class ItemData(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemData
    """

    def __init__(self):
        super().__init__()
        self.set_name("ItemData")
        
        self._Value = None
        
        self._Query = None
        
        self._AuditRecord = None
        
        self._Signature = None
        
        self._Annotation = None
        
        self._ItemOID = None
        
        self._TransactionType = None
        
        self._IsNull = None
        

    
    @property
    def Value(self):
        """
        ManyElements
        """
        if self._Value is None:
            self._Value = Value()
        return self._Value
    
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
    def ItemOID(self):
        """
        Attribute
        """
        if self._ItemOID is None:
            self._ItemOID = ItemOID()
        return self._ItemOID
    
    @property
    def TransactionType(self):
        """
        Attribute
        """
        if self._TransactionType is None:
            self._TransactionType = TransactionType()
        return self._TransactionType
    
    @property
    def IsNull(self):
        """
        Attribute
        """
        if self._IsNull is None:
            self._IsNull = IsNull()
        return self._IsNull
    