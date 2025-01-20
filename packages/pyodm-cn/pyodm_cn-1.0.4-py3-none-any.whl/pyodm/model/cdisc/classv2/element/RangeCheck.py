
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Comparator import Comparator

from pyodm.model.cdisc.classv2.attribute.SoftHard import SoftHard

from pyodm.model.cdisc.classv2.attribute.ItemOID import ItemOID


from pyodm.model.cdisc.classv2.element.ErrorMessage import ErrorMessage


from pyodm.model.definition import ManyElements



class RangeCheck(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/RangeCheck
    """

    def __init__(self):
        super().__init__()
        self.set_name("RangeCheck")
        
        self._ErrorMessage = None
        
        self._Comparator = None
        
        self._SoftHard = None
        
        self._ItemOID = None
        

    
    @property
    def ErrorMessage(self):
        """
        ManyElements
        """
        if self._ErrorMessage is None:
            self._ErrorMessage = ErrorMessage()
        return self._ErrorMessage
    
    @property
    def Comparator(self):
        """
        Attribute
        """
        if self._Comparator is None:
            self._Comparator = Comparator()
        return self._Comparator
    
    @property
    def SoftHard(self):
        """
        Attribute
        """
        if self._SoftHard is None:
            self._SoftHard = SoftHard()
        return self._SoftHard
    
    @property
    def ItemOID(self):
        """
        Attribute
        """
        if self._ItemOID is None:
            self._ItemOID = ItemOID()
        return self._ItemOID
    