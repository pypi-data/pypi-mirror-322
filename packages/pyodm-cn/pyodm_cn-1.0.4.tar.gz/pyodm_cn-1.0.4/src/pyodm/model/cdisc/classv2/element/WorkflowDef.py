
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.WorkflowStart import WorkflowStart

from pyodm.model.cdisc.classv2.element.WorkflowEnd import WorkflowEnd

from pyodm.model.cdisc.classv2.element.Transition import Transition

from pyodm.model.cdisc.classv2.element.Branching import Branching


from pyodm.model.definition import ManyElements



class WorkflowDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/WorkflowDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("WorkflowDef")
        
        self._Description = None
        
        self._WorkflowStart = None
        
        self._WorkflowEnd = None
        
        self._Transition = None
        
        self._Branching = None
        
        self._OID = None
        
        self._Name = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def WorkflowStart(self):
        """
        OneElement
        """
        if self._WorkflowStart is None:
            self._WorkflowStart = WorkflowStart()
        return self._WorkflowStart
    
    @property
    def WorkflowEnd(self):
        """
        ManyElements
        """
        if self._WorkflowEnd is None:
            self._WorkflowEnd = WorkflowEnd()
        return self._WorkflowEnd
    
    @property
    def Transition(self):
        """
        OneElement
        """
        if self._Transition is None:
            self._Transition = Transition()
        return self._Transition
    
    @property
    def Branching(self):
        """
        OneElement
        """
        if self._Branching is None:
            self._Branching = Branching()
        return self._Branching
    
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
    