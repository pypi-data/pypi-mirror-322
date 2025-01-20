
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.PublishingSet import PublishingSet

from pyodm.model.cdisc.classv2.attribute.Version import Version

from pyodm.model.cdisc.classv2.attribute.Status import Status

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID



from pyodm.model.definition import ManyElements



class Standard(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Standard
    """

    def __init__(self):
        super().__init__()
        self.set_name("Standard")
        
        self._OID = None
        
        self._Name = None
        
        self._Type = None
        
        self._PublishingSet = None
        
        self._Version = None
        
        self._Status = None
        
        self._CommentOID = None
        

    
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
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def PublishingSet(self):
        """
        Attribute
        """
        if self._PublishingSet is None:
            self._PublishingSet = PublishingSet()
        return self._PublishingSet
    
    @property
    def Version(self):
        """
        Attribute
        """
        if self._Version is None:
            self._Version = Version()
        return self._Version
    
    @property
    def Status(self):
        """
        Attribute
        """
        if self._Status is None:
            self._Status = Status()
        return self._Status
    
    @property
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    