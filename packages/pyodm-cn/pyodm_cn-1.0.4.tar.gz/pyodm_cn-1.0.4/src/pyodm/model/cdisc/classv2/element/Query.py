
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Source import Source

from pyodm.model.cdisc.classv2.attribute.Target import Target

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.State import State

from pyodm.model.cdisc.classv2.attribute.LastUpdateDatetime import LastUpdateDatetime

from pyodm.model.cdisc.classv2.attribute.Name import Name


from pyodm.model.cdisc.classv2.element.Value import Value

from pyodm.model.cdisc.classv2.element.AuditRecord import AuditRecord


from pyodm.model.definition import ManyElements



class Query(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Query
    """

    def __init__(self):
        super().__init__()
        self.set_name("Query")
        
        self._Value = None
        
        self._AuditRecord = None
        
        self._OID = None
        
        self._Source = None
        
        self._Target = None
        
        self._Type = None
        
        self._State = None
        
        self._LastUpdateDatetime = None
        
        self._Name = None
        

    
    @property
    def Value(self):
        """
        ManyElements
        """
        if self._Value is None:
            self._Value = Value()
        return self._Value
    
    @property
    def AuditRecord(self):
        """
        ManyElements
        """
        if self._AuditRecord is None:
            self._AuditRecord = AuditRecord()
        return self._AuditRecord
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    
    @property
    def Source(self):
        """
        Attribute
        """
        if self._Source is None:
            self._Source = Source()
        return self._Source
    
    @property
    def Target(self):
        """
        Attribute
        """
        if self._Target is None:
            self._Target = Target()
        return self._Target
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def State(self):
        """
        Attribute
        """
        if self._State is None:
            self._State = State()
        return self._State
    
    @property
    def LastUpdateDatetime(self):
        """
        Attribute
        """
        if self._LastUpdateDatetime is None:
            self._LastUpdateDatetime = LastUpdateDatetime()
        return self._LastUpdateDatetime
    
    @property
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    