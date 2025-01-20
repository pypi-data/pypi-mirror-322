
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.StreetName import StreetName

from pyodm.model.cdisc.classv2.element.HouseNumber import HouseNumber

from pyodm.model.cdisc.classv2.element.City import City

from pyodm.model.cdisc.classv2.element.StateProv import StateProv

from pyodm.model.cdisc.classv2.element.Country import Country

from pyodm.model.cdisc.classv2.element.PostalCode import PostalCode

from pyodm.model.cdisc.classv2.element.GeoPosition import GeoPosition

from pyodm.model.cdisc.classv2.element.OtherText import OtherText


from pyodm.model.definition import ManyElements



class Address(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Address
    """

    def __init__(self):
        super().__init__()
        self.set_name("Address")
        
        self._StreetName = None
        
        self._HouseNumber = None
        
        self._City = None
        
        self._StateProv = None
        
        self._Country = None
        
        self._PostalCode = None
        
        self._GeoPosition = None
        
        self._OtherText = None
        

    
    @property
    def StreetName(self):
        """
        OneElement
        """
        if self._StreetName is None:
            self._StreetName = StreetName()
        return self._StreetName
    
    @property
    def HouseNumber(self):
        """
        OneElement
        """
        if self._HouseNumber is None:
            self._HouseNumber = HouseNumber()
        return self._HouseNumber
    
    @property
    def City(self):
        """
        OneElement
        """
        if self._City is None:
            self._City = City()
        return self._City
    
    @property
    def StateProv(self):
        """
        OneElement
        """
        if self._StateProv is None:
            self._StateProv = StateProv()
        return self._StateProv
    
    @property
    def Country(self):
        """
        OneElement
        """
        if self._Country is None:
            self._Country = Country()
        return self._Country
    
    @property
    def PostalCode(self):
        """
        OneElement
        """
        if self._PostalCode is None:
            self._PostalCode = PostalCode()
        return self._PostalCode
    
    @property
    def GeoPosition(self):
        """
        OneElement
        """
        if self._GeoPosition is None:
            self._GeoPosition = GeoPosition()
        return self._GeoPosition
    
    @property
    def OtherText(self):
        """
        OneElement
        """
        if self._OtherText is None:
            self._OtherText = OtherText()
        return self._OtherText
    