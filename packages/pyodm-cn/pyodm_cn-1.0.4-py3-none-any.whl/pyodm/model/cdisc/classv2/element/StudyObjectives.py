
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.StudyObjective import StudyObjective


from pyodm.model.definition import OneElement



class StudyObjectives(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyObjectives
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyObjectives")
        
        self._StudyObjective = None
        

    
    @property
    def StudyObjective(self):
        """
        ManyElements
        """
        if self._StudyObjective is None:
            self._StudyObjective = StudyObjective()
        return self._StudyObjective
    