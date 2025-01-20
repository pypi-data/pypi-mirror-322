
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.StructuralElementOID import StructuralElementOID

from pyodm.model.cdisc.classv2.attribute.DurationTarget import DurationTarget

from pyodm.model.cdisc.classv2.attribute.DurationPreWindow import DurationPreWindow

from pyodm.model.cdisc.classv2.attribute.DurationPostWindow import DurationPostWindow


from pyodm.model.cdisc.classv2.element.Description import Description


from pyodm.model.definition import ManyElements



class DurationTimingConstraint(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/DurationTimingConstraint
    """

    def __init__(self):
        super().__init__()
        self.set_name("DurationTimingConstraint")
        
        self._Description = None
        
        self._OID = None
        
        self._Name = None
        
        self._StructuralElementOID = None
        
        self._DurationTarget = None
        
        self._DurationPreWindow = None
        
        self._DurationPostWindow = None
        

    
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
    def StructuralElementOID(self):
        """
        Attribute
        """
        if self._StructuralElementOID is None:
            self._StructuralElementOID = StructuralElementOID()
        return self._StructuralElementOID
    
    @property
    def DurationTarget(self):
        """
        Attribute
        """
        if self._DurationTarget is None:
            self._DurationTarget = DurationTarget()
        return self._DurationTarget
    
    @property
    def DurationPreWindow(self):
        """
        Attribute
        """
        if self._DurationPreWindow is None:
            self._DurationPreWindow = DurationPreWindow()
        return self._DurationPreWindow
    
    @property
    def DurationPostWindow(self):
        """
        Attribute
        """
        if self._DurationPostWindow is None:
            self._DurationPostWindow = DurationPostWindow()
        return self._DurationPostWindow
    