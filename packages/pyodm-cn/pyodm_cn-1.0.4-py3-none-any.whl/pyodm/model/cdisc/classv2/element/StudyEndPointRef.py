
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyEndPointOID import StudyEndPointOID

from pyodm.model.cdisc.classv2.attribute.OrderNumber import OrderNumber



from pyodm.model.definition import ManyElements



class StudyEndPointRef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEndPointRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEndPointRef")
        
        self._StudyEndPointOID = None
        
        self._OrderNumber = None
        

    
    @property
    def StudyEndPointOID(self):
        """
        Attribute
        """
        if self._StudyEndPointOID is None:
            self._StudyEndPointOID = StudyEndPointOID()
        return self._StudyEndPointOID
    
    @property
    def OrderNumber(self):
        """
        Attribute
        """
        if self._OrderNumber is None:
            self._OrderNumber = OrderNumber()
        return self._OrderNumber
    