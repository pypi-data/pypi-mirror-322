
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.StudyEventGroupOID import StudyEventGroupOID

from pyodm.model.cdisc.classv2.attribute.OrderNumber import OrderNumber

from pyodm.model.cdisc.classv2.attribute.Mandatory import Mandatory

from pyodm.model.cdisc.classv2.attribute.CollectionExceptionConditionOID import CollectionExceptionConditionOID


from pyodm.model.cdisc.classv2.element.Description import Description


from pyodm.model.definition import ManyElements



class StudyEventGroupRef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventGroupRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyEventGroupRef")
        
        self._Description = None
        
        self._StudyEventGroupOID = None
        
        self._OrderNumber = None
        
        self._Mandatory = None
        
        self._CollectionExceptionConditionOID = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def StudyEventGroupOID(self):
        """
        Attribute
        """
        if self._StudyEventGroupOID is None:
            self._StudyEventGroupOID = StudyEventGroupOID()
        return self._StudyEventGroupOID
    
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
    