
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.ID import ID


from pyodm.model.cdisc.classv2.element.UserRef import UserRef

from pyodm.model.cdisc.classv2.element.LocationRef import LocationRef

from pyodm.model.cdisc.classv2.element.SignatureRef import SignatureRef

from pyodm.model.cdisc.classv2.element.DateTimeStamp import DateTimeStamp


from pyodm.model.definition import OneElement



class Signature(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Signature
    """

    def __init__(self):
        super().__init__()
        self.set_name("Signature")
        
        self._UserRef = None
        
        self._LocationRef = None
        
        self._SignatureRef = None
        
        self._DateTimeStamp = None
        
        self._ID = None
        

    
    @property
    def UserRef(self):
        """
        OneElement
        """
        if self._UserRef is None:
            self._UserRef = UserRef()
        return self._UserRef
    
    @property
    def LocationRef(self):
        """
        OneElement
        """
        if self._LocationRef is None:
            self._LocationRef = LocationRef()
        return self._LocationRef
    
    @property
    def SignatureRef(self):
        """
        OneElement
        """
        if self._SignatureRef is None:
            self._SignatureRef = SignatureRef()
        return self._SignatureRef
    
    @property
    def DateTimeStamp(self):
        """
        OneElement
        """
        if self._DateTimeStamp is None:
            self._DateTimeStamp = DateTimeStamp()
        return self._DateTimeStamp
    
    @property
    def ID(self):
        """
        Attribute
        """
        if self._ID is None:
            self._ID = ID()
        return self._ID
    