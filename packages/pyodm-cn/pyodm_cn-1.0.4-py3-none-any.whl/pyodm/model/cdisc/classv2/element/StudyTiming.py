
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name


from pyodm.model.cdisc.classv2.element.AbsoluteTimingConstraint import AbsoluteTimingConstraint

from pyodm.model.cdisc.classv2.element.RelativeTimingConstraint import RelativeTimingConstraint

from pyodm.model.cdisc.classv2.element.TransitionTimingConstraint import TransitionTimingConstraint

from pyodm.model.cdisc.classv2.element.DurationTimingConstraint import DurationTimingConstraint


from pyodm.model.definition import ManyElements



class StudyTiming(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTiming
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyTiming")
        
        self._AbsoluteTimingConstraint = None
        
        self._RelativeTimingConstraint = None
        
        self._TransitionTimingConstraint = None
        
        self._DurationTimingConstraint = None
        
        self._OID = None
        
        self._Name = None
        

    
    @property
    def AbsoluteTimingConstraint(self):
        """
        ManyElements
        """
        if self._AbsoluteTimingConstraint is None:
            self._AbsoluteTimingConstraint = AbsoluteTimingConstraint()
        return self._AbsoluteTimingConstraint
    
    @property
    def RelativeTimingConstraint(self):
        """
        ManyElements
        """
        if self._RelativeTimingConstraint is None:
            self._RelativeTimingConstraint = RelativeTimingConstraint()
        return self._RelativeTimingConstraint
    
    @property
    def TransitionTimingConstraint(self):
        """
        ManyElements
        """
        if self._TransitionTimingConstraint is None:
            self._TransitionTimingConstraint = TransitionTimingConstraint()
        return self._TransitionTimingConstraint
    
    @property
    def DurationTimingConstraint(self):
        """
        ManyElements
        """
        if self._DurationTimingConstraint is None:
            self._DurationTimingConstraint = DurationTimingConstraint()
        return self._DurationTimingConstraint
    
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
    