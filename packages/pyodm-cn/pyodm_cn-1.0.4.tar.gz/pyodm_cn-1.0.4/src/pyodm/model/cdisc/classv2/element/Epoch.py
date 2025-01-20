
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.SequenceNumber import SequenceNumber


from pyodm.model.cdisc.classv2.element.Description import Description


from pyodm.model.definition import ManyElements



class Epoch(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Epoch
    """

    def __init__(self):
        super().__init__()
        self.set_name("Epoch")
        
        self._Description = None
        
        self._OID = None
        
        self._Name = None
        
        self._SequenceNumber = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    
    @property
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    
    @property
    def SequenceNumber(self):
        """
        Attribute
        """
        if self._SequenceNumber is None:
            self._SequenceNumber = SequenceNumber()
        return self._SequenceNumber
    