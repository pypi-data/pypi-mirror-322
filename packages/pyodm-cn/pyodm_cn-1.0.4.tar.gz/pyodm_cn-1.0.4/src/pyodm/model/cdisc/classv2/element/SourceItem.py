
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.ItemOID import ItemOID

from pyodm.model.cdisc.classv2.attribute.ItemGroupOID import ItemGroupOID

from pyodm.model.cdisc.classv2.attribute.MetaDataVersionOID import MetaDataVersionOID

from pyodm.model.cdisc.classv2.attribute.StudyOID import StudyOID

from pyodm.model.cdisc.classv2.attribute.leafID import LeafID

from pyodm.model.cdisc.classv2.attribute.Name import Name


from pyodm.model.cdisc.classv2.element.Resource import Resource

from pyodm.model.cdisc.classv2.element.Coding import Coding


from pyodm.model.definition import ManyElements



class SourceItem(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SourceItem
    """

    def __init__(self):
        super().__init__()
        self.set_name("SourceItem")
        
        self._Resource = None
        
        self._Coding = None
        
        self._ItemOID = None
        
        self._ItemGroupOID = None
        
        self._MetaDataVersionOID = None
        
        self._StudyOID = None
        
        self._leafID = None
        
        self._Name = None
        

    
    @property
    def Resource(self):
        """
        ManyElements
        """
        if self._Resource is None:
            self._Resource = Resource()
        return self._Resource
    
    @property
    def Coding(self):
        """
        ManyElements
        """
        if self._Coding is None:
            self._Coding = Coding()
        return self._Coding
    
    @property
    def ItemOID(self):
        """
        Attribute
        """
        if self._ItemOID is None:
            self._ItemOID = ItemOID()
        return self._ItemOID
    
    @property
    def ItemGroupOID(self):
        """
        Attribute
        """
        if self._ItemGroupOID is None:
            self._ItemGroupOID = ItemGroupOID()
        return self._ItemGroupOID
    
    @property
    def MetaDataVersionOID(self):
        """
        Attribute
        """
        if self._MetaDataVersionOID is None:
            self._MetaDataVersionOID = MetaDataVersionOID()
        return self._MetaDataVersionOID
    
    @property
    def StudyOID(self):
        """
        Attribute
        """
        if self._StudyOID is None:
            self._StudyOID = StudyOID()
        return self._StudyOID
    
    @property
    def leafID(self):
        """
        Attribute
        """
        if self._leafID is None:
            self._leafID = LeafID()
        return self._leafID
    
    @property
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    