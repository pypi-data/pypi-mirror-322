
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.ItemGroupOID import ItemGroupOID

from pyodm.model.cdisc.classv2.attribute.MethodOID import MethodOID

from pyodm.model.cdisc.classv2.attribute.OrderNumber import OrderNumber

from pyodm.model.cdisc.classv2.attribute.Mandatory import Mandatory

from pyodm.model.cdisc.classv2.attribute.CollectionExceptionConditionOID import CollectionExceptionConditionOID



from pyodm.model.definition import ManyElements



class ItemGroupRef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemGroupRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("ItemGroupRef")
        
        self._ItemGroupOID = None
        
        self._MethodOID = None
        
        self._OrderNumber = None
        
        self._Mandatory = None
        
        self._CollectionExceptionConditionOID = None
        

    
    @property
    def ItemGroupOID(self):
        """
        Attribute
        """
        if self._ItemGroupOID is None:
            self._ItemGroupOID = ItemGroupOID()
        return self._ItemGroupOID
    
    @property
    def MethodOID(self):
        """
        Attribute
        """
        if self._MethodOID is None:
            self._MethodOID = MethodOID()
        return self._MethodOID
    
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
    