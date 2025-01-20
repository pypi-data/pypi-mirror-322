
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Longitude import Longitude

from pyodm.model.cdisc.classv2.attribute.Latitude import Latitude

from pyodm.model.cdisc.classv2.attribute.Altitude import Altitude



from pyodm.model.definition import OneElement



class GeoPosition(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/GeoPosition
    """

    def __init__(self):
        super().__init__()
        self.set_name("GeoPosition")
        
        self._Longitude = None
        
        self._Latitude = None
        
        self._Altitude = None
        

    
    @property
    def Longitude(self):
        """
        Attribute
        """
        if self._Longitude is None:
            self._Longitude = Longitude()
        return self._Longitude
    
    @property
    def Latitude(self):
        """
        Attribute
        """
        if self._Latitude is None:
            self._Latitude = Latitude()
        return self._Latitude
    
    @property
    def Altitude(self):
        """
        Attribute
        """
        if self._Altitude is None:
            self._Altitude = Altitude()
        return self._Altitude
    