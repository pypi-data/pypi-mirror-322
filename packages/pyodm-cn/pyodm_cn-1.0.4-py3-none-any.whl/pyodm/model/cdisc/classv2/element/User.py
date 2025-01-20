
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.UserType import UserType

from pyodm.model.cdisc.classv2.attribute.OrganizationOID import OrganizationOID

from pyodm.model.cdisc.classv2.attribute.LocationOID import LocationOID


from pyodm.model.cdisc.classv2.element.UserName import UserName

from pyodm.model.cdisc.classv2.element.Prefix import Prefix

from pyodm.model.cdisc.classv2.element.Suffix import Suffix

from pyodm.model.cdisc.classv2.element.FullName import FullName

from pyodm.model.cdisc.classv2.element.GivenName import GivenName

from pyodm.model.cdisc.classv2.element.FamilyName import FamilyName

from pyodm.model.cdisc.classv2.element.Image import Image

from pyodm.model.cdisc.classv2.element.Address import Address

from pyodm.model.cdisc.classv2.element.Telecom import Telecom


from pyodm.model.definition import ManyElements



class User(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/User
    """

    def __init__(self):
        super().__init__()
        self.set_name("User")
        
        self._UserName = None
        
        self._Prefix = None
        
        self._Suffix = None
        
        self._FullName = None
        
        self._GivenName = None
        
        self._FamilyName = None
        
        self._Image = None
        
        self._Address = None
        
        self._Telecom = None
        
        self._OID = None
        
        self._UserType = None
        
        self._OrganizationOID = None
        
        self._LocationOID = None
        

    
    @property
    def UserName(self):
        """
        OneElement
        """
        if self._UserName is None:
            self._UserName = UserName()
        return self._UserName
    
    @property
    def Prefix(self):
        """
        OneElement
        """
        if self._Prefix is None:
            self._Prefix = Prefix()
        return self._Prefix
    
    @property
    def Suffix(self):
        """
        OneElement
        """
        if self._Suffix is None:
            self._Suffix = Suffix()
        return self._Suffix
    
    @property
    def FullName(self):
        """
        OneElement
        """
        if self._FullName is None:
            self._FullName = FullName()
        return self._FullName
    
    @property
    def GivenName(self):
        """
        OneElement
        """
        if self._GivenName is None:
            self._GivenName = GivenName()
        return self._GivenName
    
    @property
    def FamilyName(self):
        """
        OneElement
        """
        if self._FamilyName is None:
            self._FamilyName = FamilyName()
        return self._FamilyName
    
    @property
    def Image(self):
        """
        OneElement
        """
        if self._Image is None:
            self._Image = Image()
        return self._Image
    
    @property
    def Address(self):
        """
        ManyElements
        """
        if self._Address is None:
            self._Address = Address()
        return self._Address
    
    @property
    def Telecom(self):
        """
        ManyElements
        """
        if self._Telecom is None:
            self._Telecom = Telecom()
        return self._Telecom
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    
    @property
    def UserType(self):
        """
        Attribute
        """
        if self._UserType is None:
            self._UserType = UserType()
        return self._UserType
    
    @property
    def OrganizationOID(self):
        """
        Attribute
        """
        if self._OrganizationOID is None:
            self._OrganizationOID = OrganizationOID()
        return self._OrganizationOID
    
    @property
    def LocationOID(self):
        """
        Attribute
        """
        if self._LocationOID is None:
            self._LocationOID = LocationOID()
        return self._LocationOID
    