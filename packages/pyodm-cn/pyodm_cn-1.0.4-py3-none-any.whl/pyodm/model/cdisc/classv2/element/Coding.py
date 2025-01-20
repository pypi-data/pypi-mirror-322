
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Code import Code

from pyodm.model.cdisc.classv2.attribute.System import System

from pyodm.model.cdisc.classv2.attribute.SystemName import SystemName

from pyodm.model.cdisc.classv2.attribute.SystemVersion import SystemVersion

from pyodm.model.cdisc.classv2.attribute.Label import Label

from pyodm.model.cdisc.classv2.attribute.href import Href

from pyodm.model.cdisc.classv2.attribute.ref import Ref

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID



from pyodm.model.definition import ManyElements



class Coding(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Coding
    """

    def __init__(self):
        super().__init__()
        self.set_name("Coding")
        
        self._Code = None
        
        self._System = None
        
        self._SystemName = None
        
        self._SystemVersion = None
        
        self._Label = None
        
        self._href = None
        
        self._ref = None
        
        self._CommentOID = None
        

    
    @property
    def Code(self):
        """
        Attribute
        """
        if self._Code is None:
            self._Code = Code()
        return self._Code
    
    @property
    def System(self):
        """
        Attribute
        """
        if self._System is None:
            self._System = System()
        return self._System
    
    @property
    def SystemName(self):
        """
        Attribute
        """
        if self._SystemName is None:
            self._SystemName = SystemName()
        return self._SystemName
    
    @property
    def SystemVersion(self):
        """
        Attribute
        """
        if self._SystemVersion is None:
            self._SystemVersion = SystemVersion()
        return self._SystemVersion
    
    @property
    def Label(self):
        """
        Attribute
        """
        if self._Label is None:
            self._Label = Label()
        return self._Label
    
    @property
    def href(self):
        """
        Attribute
        """
        if self._href is None:
            self._href = Href()
        return self._href
    
    @property
    def ref(self):
        """
        Attribute
        """
        if self._ref is None:
            self._ref = Ref()
        return self._ref
    
    @property
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    