
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Role import Role

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.LocationOID import LocationOID

from pyodm.model.cdisc.classv2.attribute.PartOfOrganizationOID import PartOfOrganizationOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.Address import Address

from pyodm.model.cdisc.classv2.element.Telecom import Telecom


from pyodm.model.definition import ManyElements



class Organization(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Organization
    """

    def __init__(self):
        super().__init__()
        self.set_name("Organization")
        
        self._Description = None
        
        self._Address = None
        
        self._Telecom = None
        
        self._OID = None
        
        self._Name = None
        
        self._Role = None
        
        self._Type = None
        
        self._LocationOID = None
        
        self._PartOfOrganizationOID = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
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
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    
    @property
    def Role(self):
        """
        Attribute
        """
        if self._Role is None:
            self._Role = Role()
        return self._Role
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def LocationOID(self):
        """
        Attribute
        """
        if self._LocationOID is None:
            self._LocationOID = LocationOID()
        return self._LocationOID
    
    @property
    def PartOfOrganizationOID(self):
        """
        Attribute
        """
        if self._PartOfOrganizationOID is None:
            self._PartOfOrganizationOID = PartOfOrganizationOID()
        return self._PartOfOrganizationOID
    