
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.StudySummary import StudySummary

from pyodm.model.cdisc.classv2.element.StudyStructure import StudyStructure

from pyodm.model.cdisc.classv2.element.TrialPhase import TrialPhase

from pyodm.model.cdisc.classv2.element.StudyTimings import StudyTimings

from pyodm.model.cdisc.classv2.element.StudyIndications import StudyIndications

from pyodm.model.cdisc.classv2.element.StudyInterventions import StudyInterventions

from pyodm.model.cdisc.classv2.element.StudyObjectives import StudyObjectives

from pyodm.model.cdisc.classv2.element.StudyEndPoints import StudyEndPoints

from pyodm.model.cdisc.classv2.element.StudyTargetPopulation import StudyTargetPopulation

from pyodm.model.cdisc.classv2.element.StudyEstimands import StudyEstimands

from pyodm.model.cdisc.classv2.element.InclusionExclusionCriteria import InclusionExclusionCriteria

from pyodm.model.cdisc.classv2.element.StudyEventGroupRef import StudyEventGroupRef

from pyodm.model.cdisc.classv2.element.WorkflowRef import WorkflowRef

from pyodm.model.cdisc.classv2.element.Alias import Alias


from pyodm.model.definition import ManyElements



class Protocol(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Protocol
    """

    def __init__(self):
        super().__init__()
        self.set_name("Protocol")
        
        self._Description = None
        
        self._StudySummary = None
        
        self._StudyStructure = None
        
        self._TrialPhase = None
        
        self._StudyTimings = None
        
        self._StudyIndications = None
        
        self._StudyInterventions = None
        
        self._StudyObjectives = None
        
        self._StudyEndPoints = None
        
        self._StudyTargetPopulation = None
        
        self._StudyEstimands = None
        
        self._InclusionExclusionCriteria = None
        
        self._StudyEventGroupRef = None
        
        self._WorkflowRef = None
        
        self._Alias = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def StudySummary(self):
        """
        OneElement
        """
        if self._StudySummary is None:
            self._StudySummary = StudySummary()
        return self._StudySummary
    
    @property
    def StudyStructure(self):
        """
        OneElement
        """
        if self._StudyStructure is None:
            self._StudyStructure = StudyStructure()
        return self._StudyStructure
    
    @property
    def TrialPhase(self):
        """
        OneElement
        """
        if self._TrialPhase is None:
            self._TrialPhase = TrialPhase()
        return self._TrialPhase
    
    @property
    def StudyTimings(self):
        """
        OneElement
        """
        if self._StudyTimings is None:
            self._StudyTimings = StudyTimings()
        return self._StudyTimings
    
    @property
    def StudyIndications(self):
        """
        OneElement
        """
        if self._StudyIndications is None:
            self._StudyIndications = StudyIndications()
        return self._StudyIndications
    
    @property
    def StudyInterventions(self):
        """
        OneElement
        """
        if self._StudyInterventions is None:
            self._StudyInterventions = StudyInterventions()
        return self._StudyInterventions
    
    @property
    def StudyObjectives(self):
        """
        OneElement
        """
        if self._StudyObjectives is None:
            self._StudyObjectives = StudyObjectives()
        return self._StudyObjectives
    
    @property
    def StudyEndPoints(self):
        """
        OneElement
        """
        if self._StudyEndPoints is None:
            self._StudyEndPoints = StudyEndPoints()
        return self._StudyEndPoints
    
    @property
    def StudyTargetPopulation(self):
        """
        OneElement
        """
        if self._StudyTargetPopulation is None:
            self._StudyTargetPopulation = StudyTargetPopulation()
        return self._StudyTargetPopulation
    
    @property
    def StudyEstimands(self):
        """
        OneElement
        """
        if self._StudyEstimands is None:
            self._StudyEstimands = StudyEstimands()
        return self._StudyEstimands
    
    @property
    def InclusionExclusionCriteria(self):
        """
        OneElement
        """
        if self._InclusionExclusionCriteria is None:
            self._InclusionExclusionCriteria = InclusionExclusionCriteria()
        return self._InclusionExclusionCriteria
    
    @property
    def StudyEventGroupRef(self):
        """
        ManyElements
        """
        if self._StudyEventGroupRef is None:
            self._StudyEventGroupRef = StudyEventGroupRef()
        return self._StudyEventGroupRef
    
    @property
    def WorkflowRef(self):
        """
        ManyElements
        """
        if self._WorkflowRef is None:
            self._WorkflowRef = WorkflowRef()
        return self._WorkflowRef
    
    @property
    def Alias(self):
        """
        ManyElements
        """
        if self._Alias is None:
            self._Alias = Alias()
        return self._Alias
    