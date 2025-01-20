
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.TransitionOID import TransitionOID

from pyodm.model.cdisc.classv2.attribute.MethodOID import MethodOID

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.TimepointTarget import TimepointTarget

from pyodm.model.cdisc.classv2.attribute.TimepointPreWindow import TimepointPreWindow

from pyodm.model.cdisc.classv2.attribute.TimepointPostWindow import TimepointPostWindow


from pyodm.model.cdisc.classv2.element.Description import Description


from pyodm.model.definition import ManyElements



class TransitionTimingConstraint(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/TransitionTimingConstraint
    """

    def __init__(self):
        super().__init__()
        self.set_name("TransitionTimingConstraint")
        
        self._Description = None
        
        self._OID = None
        
        self._Name = None
        
        self._TransitionOID = None
        
        self._MethodOID = None
        
        self._Type = None
        
        self._TimepointTarget = None
        
        self._TimepointPreWindow = None
        
        self._TimepointPostWindow = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
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
    def TransitionOID(self):
        """
        Attribute
        """
        if self._TransitionOID is None:
            self._TransitionOID = TransitionOID()
        return self._TransitionOID
    
    @property
    def MethodOID(self):
        """
        Attribute
        """
        if self._MethodOID is None:
            self._MethodOID = MethodOID()
        return self._MethodOID
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def TimepointTarget(self):
        """
        Attribute
        """
        if self._TimepointTarget is None:
            self._TimepointTarget = TimepointTarget()
        return self._TimepointTarget
    
    @property
    def TimepointPreWindow(self):
        """
        Attribute
        """
        if self._TimepointPreWindow is None:
            self._TimepointPreWindow = TimepointPreWindow()
        return self._TimepointPreWindow
    
    @property
    def TimepointPostWindow(self):
        """
        Attribute
        """
        if self._TimepointPostWindow is None:
            self._TimepointPostWindow = TimepointPostWindow()
        return self._TimepointPostWindow
    