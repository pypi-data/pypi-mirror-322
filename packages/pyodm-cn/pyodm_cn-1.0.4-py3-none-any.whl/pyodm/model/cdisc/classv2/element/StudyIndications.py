
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.StudyIndication import StudyIndication


from pyodm.model.definition import OneElement



class StudyIndications(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyIndications
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyIndications")
        
        self._StudyIndication = None
        

    
    @property
    def StudyIndication(self):
        """
        ManyElements
        """
        if self._StudyIndication is None:
            self._StudyIndication = StudyIndication()
        return self._StudyIndication
    