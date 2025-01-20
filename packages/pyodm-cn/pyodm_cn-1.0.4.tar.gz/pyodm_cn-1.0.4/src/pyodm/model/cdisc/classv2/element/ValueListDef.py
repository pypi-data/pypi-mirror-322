
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.ItemRef import ItemRef


from pyodm.model.definition import ManyElements



class ValueListDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ValueListDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("ValueListDef")
        
        self._Description = None
        
        self._ItemRef = None
        
        self._OID = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def ItemRef(self):
        """
        ManyElements
        """
        if self._ItemRef is None:
            self._ItemRef = ItemRef()
        return self._ItemRef
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    