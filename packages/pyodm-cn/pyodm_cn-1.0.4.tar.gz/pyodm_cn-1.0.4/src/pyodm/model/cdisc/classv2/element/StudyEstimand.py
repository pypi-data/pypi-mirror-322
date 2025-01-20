
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Level import Level


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.StudyTargetPopulationRef import StudyTargetPopulationRef

from pyodm.model.cdisc.classv2.element.StudyInterventionRef import StudyInterventionRef

from pyodm.model.cdisc.classv2.element.StudyEndPointRef import StudyEndPointRef

from pyodm.model.cdisc.classv2.element.IntercurrentEvent import IntercurrentEvent

from pyodm.model.cdisc.classv2.element.SummaryMeasure import SummaryMeasure


from pyodm.model.definition import ManyElements



class StudyEstimand(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEstimand
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEstimand")
        
        self._Description = None
        
        self._StudyTargetPopulationRef = None
        
        self._StudyInterventionRef = None
        
        self._StudyEndPointRef = None
        
        self._IntercurrentEvent = None
        
        self._SummaryMeasure = None
        
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
    def StudyTargetPopulationRef(self):
        """
        OneElement
        """
        if self._StudyTargetPopulationRef is None:
            self._StudyTargetPopulationRef = StudyTargetPopulationRef()
        return self._StudyTargetPopulationRef
    
    @property
    def StudyInterventionRef(self):
        """
        OneElement
        """
        if self._StudyInterventionRef is None:
            self._StudyInterventionRef = StudyInterventionRef()
        return self._StudyInterventionRef
    
    @property
    def StudyEndPointRef(self):
        """
        ManyElements
        """
        if self._StudyEndPointRef is None:
            self._StudyEndPointRef = StudyEndPointRef()
        return self._StudyEndPointRef
    
    @property
    def IntercurrentEvent(self):
        """
        ManyElements
        """
        if self._IntercurrentEvent is None:
            self._IntercurrentEvent = IntercurrentEvent()
        return self._IntercurrentEvent
    
    @property
    def SummaryMeasure(self):
        """
        OneElement
        """
        if self._SummaryMeasure is None:
            self._SummaryMeasure = SummaryMeasure()
        return self._SummaryMeasure
    
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
    