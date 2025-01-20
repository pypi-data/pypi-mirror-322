
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyOID import StudyOID

from pyodm.model.cdisc.classv2.attribute.SubjectKey import SubjectKey

from pyodm.model.cdisc.classv2.attribute.MetaDataVersionOID import MetaDataVersionOID

from pyodm.model.cdisc.classv2.attribute.StudyEventOID import StudyEventOID

from pyodm.model.cdisc.classv2.attribute.StudyEventRepeatKey import StudyEventRepeatKey

from pyodm.model.cdisc.classv2.attribute.ItemGroupOID import ItemGroupOID

from pyodm.model.cdisc.classv2.attribute.ItemGroupRepeatKey import ItemGroupRepeatKey

from pyodm.model.cdisc.classv2.attribute.ItemOID import ItemOID



from pyodm.model.definition import ManyElements



class KeySet(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/KeySet
    """

    def __init__(self):
        super().__init__()
        self.set_name("KeySet")
        
        self._StudyOID = None
        
        self._SubjectKey = None
        
        self._MetaDataVersionOID = None
        
        self._StudyEventOID = None
        
        self._StudyEventRepeatKey = None
        
        self._ItemGroupOID = None
        
        self._ItemGroupRepeatKey = None
        
        self._ItemOID = None
        

    
    @property
    def StudyOID(self):
        """
        Attribute
        """
        if self._StudyOID is None:
            self._StudyOID = StudyOID()
        return self._StudyOID
    
    @property
    def SubjectKey(self):
        """
        Attribute
        """
        if self._SubjectKey is None:
            self._SubjectKey = SubjectKey()
        return self._SubjectKey
    
    @property
    def MetaDataVersionOID(self):
        """
        Attribute
        """
        if self._MetaDataVersionOID is None:
            self._MetaDataVersionOID = MetaDataVersionOID()
        return self._MetaDataVersionOID
    
    @property
    def StudyEventOID(self):
        """
        Attribute
        """
        if self._StudyEventOID is None:
            self._StudyEventOID = StudyEventOID()
        return self._StudyEventOID
    
    @property
    def StudyEventRepeatKey(self):
        """
        Attribute
        """
        if self._StudyEventRepeatKey is None:
            self._StudyEventRepeatKey = StudyEventRepeatKey()
        return self._StudyEventRepeatKey
    
    @property
    def ItemGroupOID(self):
        """
        Attribute
        """
        if self._ItemGroupOID is None:
            self._ItemGroupOID = ItemGroupOID()
        return self._ItemGroupOID
    
    @property
    def ItemGroupRepeatKey(self):
        """
        Attribute
        """
        if self._ItemGroupRepeatKey is None:
            self._ItemGroupRepeatKey = ItemGroupRepeatKey()
        return self._ItemGroupRepeatKey
    
    @property
    def ItemOID(self):
        """
        Attribute
        """
        if self._ItemOID is None:
            self._ItemOID = ItemOID()
        return self._ItemOID
    