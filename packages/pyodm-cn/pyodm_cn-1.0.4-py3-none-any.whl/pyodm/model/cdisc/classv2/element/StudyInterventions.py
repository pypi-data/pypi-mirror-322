
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.StudyIntervention import StudyIntervention


from pyodm.model.definition import OneElement



class StudyInterventions(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyInterventions
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyInterventions")
        
        self._StudyIntervention = None
        

    
    @property
    def StudyIntervention(self):
        """
        ManyElements
        """
        if self._StudyIntervention is None:
            self._StudyIntervention = StudyIntervention()
        return self._StudyIntervention
    