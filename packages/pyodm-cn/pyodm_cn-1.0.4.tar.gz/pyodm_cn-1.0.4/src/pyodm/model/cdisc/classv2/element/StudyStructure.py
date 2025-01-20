
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.Arm import Arm

from pyodm.model.cdisc.classv2.element.Epoch import Epoch

from pyodm.model.cdisc.classv2.element.WorkflowRef import WorkflowRef


from pyodm.model.definition import OneElement



class StudyStructure(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyStructure
    """

    def __init__(self):
        super().__init__()
        self.set_name("StudyStructure")
        
        self._Description = None
        
        self._Arm = None
        
        self._Epoch = None
        
        self._WorkflowRef = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def Arm(self):
        """
        ManyElements
        """
        if self._Arm is None:
            self._Arm = Arm()
        return self._Arm
    
    @property
    def Epoch(self):
        """
        ManyElements
        """
        if self._Epoch is None:
            self._Epoch = Epoch()
        return self._Epoch
    
    @property
    def WorkflowRef(self):
        """
        ManyElements
        """
        if self._WorkflowRef is None:
            self._WorkflowRef = WorkflowRef()
        return self._WorkflowRef
    