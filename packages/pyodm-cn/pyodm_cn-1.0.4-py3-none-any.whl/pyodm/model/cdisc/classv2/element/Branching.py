
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Type import Type


from pyodm.model.cdisc.classv2.element.TargetTransition import TargetTransition

from pyodm.model.cdisc.classv2.element.DefaultTransition import DefaultTransition


from pyodm.model.definition import OneElement



class Branching(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Branching
    """

    def __init__(self):
        super().__init__()
        self.set_name("Branching")
        
        self._TargetTransition = None
        
        self._DefaultTransition = None
        
        self._OID = None
        
        self._Name = None
        
        self._Type = None
        

    
    @property
    def TargetTransition(self):
        """
        ManyElements
        """
        if self._TargetTransition is None:
            self._TargetTransition = TargetTransition()
        return self._TargetTransition
    
    @property
    def DefaultTransition(self):
        """
        ManyElements
        """
        if self._DefaultTransition is None:
            self._DefaultTransition = DefaultTransition()
        return self._DefaultTransition
    
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
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    