
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Level import Level


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.StudyEndPointRef import StudyEndPointRef


from pyodm.model.definition import ManyElements



class StudyObjective(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyObjective
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyObjective")
        
        self._Description = None
        
        self._StudyEndPointRef = None
        
        self._OID = None
        
        self._Name = None
        
        self._Level = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def StudyEndPointRef(self):
        """
        ManyElements
        """
        if self._StudyEndPointRef is None:
            self._StudyEndPointRef = StudyEndPointRef()
        return self._StudyEndPointRef
    
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
    def Level(self):
        """
        Attribute
        """
        if self._Level is None:
            self._Level = Level()
        return self._Level
    