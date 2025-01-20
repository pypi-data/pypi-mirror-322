
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.PredecessorOID import PredecessorOID

from pyodm.model.cdisc.classv2.attribute.SuccessorOID import SuccessorOID

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.TimepointRelativeTarget import TimepointRelativeTarget

from pyodm.model.cdisc.classv2.attribute.TimepointPreWindow import TimepointPreWindow

from pyodm.model.cdisc.classv2.attribute.TimepointPostWindow import TimepointPostWindow


from pyodm.model.cdisc.classv2.element.Description import Description


from pyodm.model.definition import ManyElements



class RelativeTimingConstraint(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/RelativeTimingConstraint
    """

    def __init__(self):
        super().__init__()
        self.set_name("RelativeTimingConstraint")
        
        self._Description = None
        
        self._OID = None
        
        self._Name = None
        
        self._PredecessorOID = None
        
        self._SuccessorOID = None
        
        self._Type = None
        
        self._TimepointRelativeTarget = None
        
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
    def PredecessorOID(self):
        """
        Attribute
        """
        if self._PredecessorOID is None:
            self._PredecessorOID = PredecessorOID()
        return self._PredecessorOID
    
    @property
    def SuccessorOID(self):
        """
        Attribute
        """
        if self._SuccessorOID is None:
            self._SuccessorOID = SuccessorOID()
        return self._SuccessorOID
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def TimepointRelativeTarget(self):
        """
        Attribute
        """
        if self._TimepointRelativeTarget is None:
            self._TimepointRelativeTarget = TimepointRelativeTarget()
        return self._TimepointRelativeTarget
    
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
    