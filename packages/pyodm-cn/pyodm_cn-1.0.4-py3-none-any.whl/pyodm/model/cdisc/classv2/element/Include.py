
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyOID import StudyOID

from pyodm.model.cdisc.classv2.attribute.MetaDataVersionOID import MetaDataVersionOID

from pyodm.model.cdisc.classv2.attribute.href import Href



from pyodm.model.definition import ManyElements



class Include(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Include
    """

    def __init__(self):
        super().__init__()
        self.set_name("Include")
        
        self._StudyOID = None
        
        self._MetaDataVersionOID = None
        
        self._href = None
        

    
    @property
    def StudyOID(self):
        """
        Attribute
        """
        if self._StudyOID is None:
            self._StudyOID = StudyOID()
        return self._StudyOID
    
    @property
    def MetaDataVersionOID(self):
        """
        Attribute
        """
        if self._MetaDataVersionOID is None:
            self._MetaDataVersionOID = MetaDataVersionOID()
        return self._MetaDataVersionOID
    
    @property
    def href(self):
        """
        Attribute
        """
        if self._href is None:
            self._href = Href()
        return self._href
    