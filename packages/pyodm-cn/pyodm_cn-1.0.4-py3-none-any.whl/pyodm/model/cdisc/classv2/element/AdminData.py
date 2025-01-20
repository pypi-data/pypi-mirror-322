
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyOID import StudyOID


from pyodm.model.cdisc.classv2.element.User import User

from pyodm.model.cdisc.classv2.element.Organization import Organization

from pyodm.model.cdisc.classv2.element.Location import Location

from pyodm.model.cdisc.classv2.element.SignatureDef import SignatureDef


from pyodm.model.definition import ManyElements



class AdminData(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/AdminData
    """

    def __init__(self):
        super().__init__()
        self.set_name("AdminData")
        
        self._User = None
        
        self._Organization = None
        
        self._Location = None
        
        self._SignatureDef = None
        
        self._StudyOID = None
        

    
    @property
    def User(self):
        """
        ManyElements
        """
        if self._User is None:
            self._User = User()
        return self._User
    
    @property
    def Organization(self):
        """
        ManyElements
        """
        if self._Organization is None:
            self._Organization = Organization()
        return self._Organization
    
    @property
    def Location(self):
        """
        ManyElements
        """
        if self._Location is None:
            self._Location = Location()
        return self._Location
    
    @property
    def SignatureDef(self):
        """
        ManyElements
        """
        if self._SignatureDef is None:
            self._SignatureDef = SignatureDef()
        return self._SignatureDef
    
    @property
    def StudyOID(self):
        """
        Attribute
        """
        if self._StudyOID is None:
            self._StudyOID = StudyOID()
        return self._StudyOID
    