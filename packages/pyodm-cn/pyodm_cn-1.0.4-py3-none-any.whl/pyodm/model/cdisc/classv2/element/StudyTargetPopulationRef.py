
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyTargetPopulationOID import StudyTargetPopulationOID



from pyodm.model.definition import OneElement



class StudyTargetPopulationRef(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTargetPopulationRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyTargetPopulationRef")
        
        self._StudyTargetPopulationOID = None
        

    
    @property
    def StudyTargetPopulationOID(self):
        """
        Attribute
        """
        if self._StudyTargetPopulationOID is None:
            self._StudyTargetPopulationOID = StudyTargetPopulationOID()
        return self._StudyTargetPopulationOID
    