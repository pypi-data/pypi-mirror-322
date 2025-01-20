
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.LocationOID import LocationOID



from pyodm.model.definition import OneElement



class LocationRef(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/LocationRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("LocationRef")
        
        self._LocationOID = None
        

    
    @property
    def LocationOID(self):
        """
        Attribute
        """
        if self._LocationOID is None:
            self._LocationOID = LocationOID()
        return self._LocationOID
    