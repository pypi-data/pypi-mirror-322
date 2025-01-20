
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.StudyName import StudyName

from pyodm.model.cdisc.classv2.attribute.ProtocolName import ProtocolName

from pyodm.model.cdisc.classv2.attribute.VersionID import VersionID

from pyodm.model.cdisc.classv2.attribute.VersionName import VersionName

from pyodm.model.cdisc.classv2.attribute.Status import Status


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.MetaDataVersion import MetaDataVersion


from pyodm.model.definition import ManyElements



class Study(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Study
    """

    def __init__(self):
        super().__init__()
        self.set_name("Study")
        
        self._Description = None
        
        self._MetaDataVersion = None
        
        self._OID = None
        
        self._StudyName = None
        
        self._ProtocolName = None
        
        self._VersionID = None
        
        self._VersionName = None
        
        self._Status = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def MetaDataVersion(self):
        """
        ManyElements
        """
        if self._MetaDataVersion is None:
            self._MetaDataVersion = MetaDataVersion()
        return self._MetaDataVersion
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    
    @property
    def StudyName(self):
        """
        Attribute
        """
        if self._StudyName is None:
            self._StudyName = StudyName()
        return self._StudyName
    
    @property
    def ProtocolName(self):
        """
        Attribute
        """
        if self._ProtocolName is None:
            self._ProtocolName = ProtocolName()
        return self._ProtocolName
    
    @property
    def VersionID(self):
        """
        Attribute
        """
        if self._VersionID is None:
            self._VersionID = VersionID()
        return self._VersionID
    
    @property
    def VersionName(self):
        """
        Attribute
        """
        if self._VersionName is None:
            self._VersionName = VersionName()
        return self._VersionName
    
    @property
    def Status(self):
        """
        Attribute
        """
        if self._Status is None:
            self._Status = Status()
        return self._Status
    