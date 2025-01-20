
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Role import Role

from pyodm.model.cdisc.classv2.attribute.OrganizationOID import OrganizationOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.MetaDataVersionRef import MetaDataVersionRef

from pyodm.model.cdisc.classv2.element.Address import Address

from pyodm.model.cdisc.classv2.element.Telecom import Telecom

from pyodm.model.cdisc.classv2.element.Query import Query


from pyodm.model.definition import ManyElements



class Location(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Location
    """

    def __init__(self):
        super().__init__()
        self.set_name("Location")
        
        self._Description = None
        
        self._MetaDataVersionRef = None
        
        self._Address = None
        
        self._Telecom = None
        
        self._Query = None
        
        self._OID = None
        
        self._Name = None
        
        self._Role = None
        
        self._OrganizationOID = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def MetaDataVersionRef(self):
        """
        ManyElements
        """
        if self._MetaDataVersionRef is None:
            self._MetaDataVersionRef = MetaDataVersionRef()
        return self._MetaDataVersionRef
    
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
    def Query(self):
        """
        ManyElements
        """
        if self._Query is None:
            self._Query = Query()
        return self._Query
    
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
    def OrganizationOID(self):
        """
        Attribute
        """
        if self._OrganizationOID is None:
            self._OrganizationOID = OrganizationOID()
        return self._OrganizationOID
    