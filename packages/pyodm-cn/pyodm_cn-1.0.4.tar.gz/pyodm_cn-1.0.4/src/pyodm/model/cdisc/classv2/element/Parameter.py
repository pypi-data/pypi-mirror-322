
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.DataType import DataType

from pyodm.model.cdisc.classv2.attribute.Definition import Definition

from pyodm.model.cdisc.classv2.attribute.OrderNumber import OrderNumber



from pyodm.model.definition import ManyElements



class Parameter(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Parameter
    """

    def __init__(self):
        super().__init__()
        self.set_name("Parameter")
        
        self._Name = None
        
        self._DataType = None
        
        self._Definition = None
        
        self._OrderNumber = None
        

    
    @property
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    
    @property
    def DataType(self):
        """
        Attribute
        """
        if self._DataType is None:
            self._DataType = DataType()
        return self._DataType
    
    @property
    def Definition(self):
        """
        Attribute
        """
        if self._Definition is None:
            self._Definition = Definition()
        return self._Definition
    
    @property
    def OrderNumber(self):
        """
        Attribute
        """
        if self._OrderNumber is None:
            self._OrderNumber = OrderNumber()
        return self._OrderNumber
    