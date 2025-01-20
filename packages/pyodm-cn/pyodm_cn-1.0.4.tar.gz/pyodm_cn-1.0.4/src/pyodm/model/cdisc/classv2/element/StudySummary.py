
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.StudyParameter import StudyParameter


from pyodm.model.definition import OneElement



class StudySummary(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudySummary
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudySummary")
        
        self._StudyParameter = None
        

    
    @property
    def StudyParameter(self):
        """
        ManyElements
        """
        if self._StudyParameter is None:
            self._StudyParameter = StudyParameter()
        return self._StudyParameter
    