
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.EditPoint import EditPoint

from pyodm.model.cdisc.classv2.attribute.UsedMethod import UsedMethod


from pyodm.model.cdisc.classv2.element.UserRef import UserRef

from pyodm.model.cdisc.classv2.element.LocationRef import LocationRef

from pyodm.model.cdisc.classv2.element.DateTimeStamp import DateTimeStamp

from pyodm.model.cdisc.classv2.element.ReasonForChange import ReasonForChange

from pyodm.model.cdisc.classv2.element.SourceID import SourceID


from pyodm.model.definition import ManyElements



class AuditRecord(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/AuditRecord
    """

    def __init__(self):
        super().__init__()
        self.set_name("AuditRecord")
        
        self._UserRef = None
        
        self._LocationRef = None
        
        self._DateTimeStamp = None
        
        self._ReasonForChange = None
        
        self._SourceID = None
        
        self._EditPoint = None
        
        self._UsedMethod = None
        

    
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
    def DateTimeStamp(self):
        """
        OneElement
        """
        if self._DateTimeStamp is None:
            self._DateTimeStamp = DateTimeStamp()
        return self._DateTimeStamp
    
    @property
    def ReasonForChange(self):
        """
        OneElement
        """
        if self._ReasonForChange is None:
            self._ReasonForChange = ReasonForChange()
        return self._ReasonForChange
    
    @property
    def SourceID(self):
        """
        OneElement
        """
        if self._SourceID is None:
            self._SourceID = SourceID()
        return self._SourceID
    
    @property
    def EditPoint(self):
        """
        Attribute
        """
        if self._EditPoint is None:
            self._EditPoint = EditPoint()
        return self._EditPoint
    
    @property
    def UsedMethod(self):
        """
        Attribute
        """
        if self._UsedMethod is None:
            self._UsedMethod = UsedMethod()
        return self._UsedMethod
    