
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.SourceOID import SourceOID

from pyodm.model.cdisc.classv2.attribute.TargetOID import TargetOID

from pyodm.model.cdisc.classv2.attribute.StartConditionOID import StartConditionOID

from pyodm.model.cdisc.classv2.attribute.EndConditionOID import EndConditionOID



from pyodm.model.definition import OneElement



class Transition(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Transition
    """

    def __init__(self):
        super().__init__()
        self.set_name("Transition")
        
        self._OID = None
        
        self._Name = None
        
        self._SourceOID = None
        
        self._TargetOID = None
        
        self._StartConditionOID = None
        
        self._EndConditionOID = None
        

    
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
    def SourceOID(self):
        """
        Attribute
        """
        if self._SourceOID is None:
            self._SourceOID = SourceOID()
        return self._SourceOID
    
    @property
    def TargetOID(self):
        """
        Attribute
        """
        if self._TargetOID is None:
            self._TargetOID = TargetOID()
        return self._TargetOID
    
    @property
    def StartConditionOID(self):
        """
        Attribute
        """
        if self._StartConditionOID is None:
            self._StartConditionOID = StartConditionOID()
        return self._StartConditionOID
    
    @property
    def EndConditionOID(self):
        """
        Attribute
        """
        if self._EndConditionOID is None:
            self._EndConditionOID = EndConditionOID()
        return self._EndConditionOID
    