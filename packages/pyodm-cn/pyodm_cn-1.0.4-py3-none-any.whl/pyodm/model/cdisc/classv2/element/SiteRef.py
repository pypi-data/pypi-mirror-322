
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.LocationOID import LocationOID



from pyodm.model.definition import OneElement



class SiteRef(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SiteRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("SiteRef")
        
        self._LocationOID = None
        

    
    @property
    def LocationOID(self):
        """
        Attribute
        """
        if self._LocationOID is None:
            self._LocationOID = LocationOID()
        return self._LocationOID
    