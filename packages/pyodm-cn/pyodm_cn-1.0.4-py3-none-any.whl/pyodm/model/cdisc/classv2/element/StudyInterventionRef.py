
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyInterventionOID import StudyInterventionOID



from pyodm.model.definition import OneElement



class StudyInterventionRef(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyInterventionRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyInterventionRef")
        
        self._StudyInterventionOID = None
        

    
    @property
    def StudyInterventionOID(self):
        """
        Attribute
        """
        if self._StudyInterventionOID is None:
            self._StudyInterventionOID = StudyInterventionOID()
        return self._StudyInterventionOID
    