
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyEventOID import StudyEventOID

from pyodm.model.cdisc.classv2.attribute.OrderNumber import OrderNumber

from pyodm.model.cdisc.classv2.attribute.Mandatory import Mandatory

from pyodm.model.cdisc.classv2.attribute.CollectionExceptionConditionOID import CollectionExceptionConditionOID



from pyodm.model.definition import OneElement



class StudyEventRef(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEventRef")
        
        self._StudyEventOID = None
        
        self._OrderNumber = None
        
        self._Mandatory = None
        
        self._CollectionExceptionConditionOID = None
        

    
    @property
    def StudyEventOID(self):
        """
        Attribute
        """
        if self._StudyEventOID is None:
            self._StudyEventOID = StudyEventOID()
        return self._StudyEventOID
    
    @property
    def OrderNumber(self):
        """
        Attribute
        """
        if self._OrderNumber is None:
            self._OrderNumber = OrderNumber()
        return self._OrderNumber
    
    @property
    def Mandatory(self):
        """
        Attribute
        """
        if self._Mandatory is None:
            self._Mandatory = Mandatory()
        return self._Mandatory
    
    @property
    def CollectionExceptionConditionOID(self):
        """
        Attribute
        """
        if self._CollectionExceptionConditionOID is None:
            self._CollectionExceptionConditionOID = CollectionExceptionConditionOID()
        return self._CollectionExceptionConditionOID
    