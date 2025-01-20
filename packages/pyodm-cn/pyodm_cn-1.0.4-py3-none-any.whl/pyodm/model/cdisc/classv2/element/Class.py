
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Name import Name


from pyodm.model.cdisc.classv2.element.SubClass import SubClass


from pyodm.model.definition import ManyElements



class Class(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Class
    """

    def __init__(self):
        super().__init__()
        self.set_name("Class")
        
        self._SubClass = None
        
        self._Name = None
        

    
    @property
    def SubClass(self):
        """
        ManyElements
        """
        if self._SubClass is None:
            self._SubClass = SubClass()
        return self._SubClass
    
    @property
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    