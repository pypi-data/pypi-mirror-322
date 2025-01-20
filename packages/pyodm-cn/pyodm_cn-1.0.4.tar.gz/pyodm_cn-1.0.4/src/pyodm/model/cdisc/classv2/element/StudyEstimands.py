
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.StudyEstimand import StudyEstimand


from pyodm.model.definition import OneElement



class StudyEstimands(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEstimands
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEstimands")
        
        self._StudyEstimand = None
        

    
    @property
    def StudyEstimand(self):
        """
        ManyElements
        """
        if self._StudyEstimand is None:
            self._StudyEstimand = StudyEstimand()
        return self._StudyEstimand
    