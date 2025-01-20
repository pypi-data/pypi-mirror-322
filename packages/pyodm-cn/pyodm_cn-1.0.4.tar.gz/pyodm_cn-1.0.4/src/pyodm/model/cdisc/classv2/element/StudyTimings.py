
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.StudyTiming import StudyTiming


from pyodm.model.definition import OneElement



class StudyTimings(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTimings
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyTimings")
        
        self._StudyTiming = None
        

    
    @property
    def StudyTiming(self):
        """
        ManyElements
        """
        if self._StudyTiming is None:
            self._StudyTiming = StudyTiming()
        return self._StudyTiming
    