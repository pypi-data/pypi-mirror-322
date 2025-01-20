
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.ItemOID import ItemOID

from pyodm.model.cdisc.classv2.attribute.KeySequence import KeySequence

from pyodm.model.cdisc.classv2.attribute.IsNonStandard import IsNonStandard

from pyodm.model.cdisc.classv2.attribute.HasNoData import HasNoData

from pyodm.model.cdisc.classv2.attribute.MethodOID import MethodOID

from pyodm.model.cdisc.classv2.attribute.UnitsItemOID import UnitsItemOID

from pyodm.model.cdisc.classv2.attribute.Repeat import Repeat

from pyodm.model.cdisc.classv2.attribute.Other import Other

from pyodm.model.cdisc.classv2.attribute.Role import Role

from pyodm.model.cdisc.classv2.attribute.RoleCodeListOID import RoleCodeListOID

from pyodm.model.cdisc.classv2.attribute.Core import Core

from pyodm.model.cdisc.classv2.attribute.PreSpecifiedValue import PreSpecifiedValue

from pyodm.model.cdisc.classv2.attribute.OrderNumber import OrderNumber

from pyodm.model.cdisc.classv2.attribute.Mandatory import Mandatory

from pyodm.model.cdisc.classv2.attribute.CollectionExceptionConditionOID import CollectionExceptionConditionOID


from pyodm.model.cdisc.classv2.element.Origin import Origin

from pyodm.model.cdisc.classv2.element.WhereClauseRef import WhereClauseRef


from pyodm.model.definition import ManyElements



class ItemRef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("ItemRef")
        
        self._Origin = None
        
        self._WhereClauseRef = None
        
        self._ItemOID = None
        
        self._KeySequence = None
        
        self._IsNonStandard = None
        
        self._HasNoData = None
        
        self._MethodOID = None
        
        self._UnitsItemOID = None
        
        self._Repeat = None
        
        self._Other = None
        
        self._Role = None
        
        self._RoleCodeListOID = None
        
        self._Core = None
        
        self._PreSpecifiedValue = None
        
        self._OrderNumber = None
        
        self._Mandatory = None
        
        self._CollectionExceptionConditionOID = None
        

    
    @property
    def Origin(self):
        """
        ManyElements
        """
        if self._Origin is None:
            self._Origin = Origin()
        return self._Origin
    
    @property
    def WhereClauseRef(self):
        """
        ManyElements
        """
        if self._WhereClauseRef is None:
            self._WhereClauseRef = WhereClauseRef()
        return self._WhereClauseRef
    
    @property
    def ItemOID(self):
        """
        Attribute
        """
        if self._ItemOID is None:
            self._ItemOID = ItemOID()
        return self._ItemOID
    
    @property
    def KeySequence(self):
        """
        Attribute
        """
        if self._KeySequence is None:
            self._KeySequence = KeySequence()
        return self._KeySequence
    
    @property
    def IsNonStandard(self):
        """
        Attribute
        """
        if self._IsNonStandard is None:
            self._IsNonStandard = IsNonStandard()
        return self._IsNonStandard
    
    @property
    def HasNoData(self):
        """
        Attribute
        """
        if self._HasNoData is None:
            self._HasNoData = HasNoData()
        return self._HasNoData
    
    @property
    def MethodOID(self):
        """
        Attribute
        """
        if self._MethodOID is None:
            self._MethodOID = MethodOID()
        return self._MethodOID
    
    @property
    def UnitsItemOID(self):
        """
        Attribute
        """
        if self._UnitsItemOID is None:
            self._UnitsItemOID = UnitsItemOID()
        return self._UnitsItemOID
    
    @property
    def Repeat(self):
        """
        Attribute
        """
        if self._Repeat is None:
            self._Repeat = Repeat()
        return self._Repeat
    
    @property
    def Other(self):
        """
        Attribute
        """
        if self._Other is None:
            self._Other = Other()
        return self._Other
    
    @property
    def Role(self):
        """
        Attribute
        """
        if self._Role is None:
            self._Role = Role()
        return self._Role
    
    @property
    def RoleCodeListOID(self):
        """
        Attribute
        """
        if self._RoleCodeListOID is None:
            self._RoleCodeListOID = RoleCodeListOID()
        return self._RoleCodeListOID
    
    @property
    def Core(self):
        """
        Attribute
        """
        if self._Core is None:
            self._Core = Core()
        return self._Core
    
    @property
    def PreSpecifiedValue(self):
        """
        Attribute
        """
        if self._PreSpecifiedValue is None:
            self._PreSpecifiedValue = PreSpecifiedValue()
        return self._PreSpecifiedValue
    
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
    