
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.StudyEndPoint import StudyEndPoint


from pyodm.model.definition import OneElement



class StudyEndPoints(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEndPoints
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEndPoints")
        
        self._StudyEndPoint = None
        

    
    @property
    def StudyEndPoint(self):
        """
        ManyElements
        """
        if self._StudyEndPoint is None:
            self._StudyEndPoint = StudyEndPoint()
        return self._StudyEndPoint
    