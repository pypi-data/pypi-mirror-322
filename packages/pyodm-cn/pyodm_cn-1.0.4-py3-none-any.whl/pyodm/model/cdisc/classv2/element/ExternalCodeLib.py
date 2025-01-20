
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Library import Library

from pyodm.model.cdisc.classv2.attribute.Method import Method

from pyodm.model.cdisc.classv2.attribute.Version import Version

from pyodm.model.cdisc.classv2.attribute.ref import Ref

from pyodm.model.cdisc.classv2.attribute.href import Href





class ExternalCodeLib(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ExternalCodeLib
    """

    def __init__(self):
        super().__init__()
        self.set_name("ExternalCodeLib")
        
        self._Library = None
        
        self._Method = None
        
        self._Version = None
        
        self._ref = None
        
        self._href = None
        

    
    @property
    def Library(self):
        """
        Attribute
        """
        if self._Library is None:
            self._Library = Library()
        return self._Library
    
    @property
    def Method(self):
        """
        Attribute
        """
        if self._Method is None:
            self._Method = Method()
        return self._Method
    
    @property
    def Version(self):
        """
        Attribute
        """
        if self._Version is None:
            self._Version = Version()
        return self._Version
    
    @property
    def ref(self):
        """
        Attribute
        """
        if self._ref is None:
            self._ref = Ref()
        return self._ref
    
    @property
    def href(self):
        """
        Attribute
        """
        if self._href is None:
            self._href = Href()
        return self._href
    