
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyOID import StudyOID

from pyodm.model.cdisc.classv2.attribute.MetaDataVersionOID import MetaDataVersionOID


from pyodm.model.cdisc.classv2.element.KeySet import KeySet

from pyodm.model.cdisc.classv2.element.Annotation import Annotation


from pyodm.model.definition import ManyElements



class Association(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Association
    """

    def __init__(self):
        super().__init__()
        self.set_name("Association")
        
        self._KeySet = None
        
        self._Annotation = None
        
        self._StudyOID = None
        
        self._MetaDataVersionOID = None
        

    
    @property
    def KeySet(self):
        """
        ManyElements
        """
        if self._KeySet is None:
            self._KeySet = KeySet()
        return self._KeySet
    
    @property
    def Annotation(self):
        """
        ManyElements
        """
        if self._Annotation is None:
            self._Annotation = Annotation()
        return self._Annotation
    
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
    