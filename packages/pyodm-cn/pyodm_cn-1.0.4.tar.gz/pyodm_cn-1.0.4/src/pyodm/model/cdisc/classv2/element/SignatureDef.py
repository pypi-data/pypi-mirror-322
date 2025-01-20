
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Methodology import Methodology


from pyodm.model.cdisc.classv2.element.Meaning import Meaning

from pyodm.model.cdisc.classv2.element.LegalReason import LegalReason


from pyodm.model.definition import ManyElements



class SignatureDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SignatureDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("SignatureDef")
        
        self._Meaning = None
        
        self._LegalReason = None
        
        self._OID = None
        
        self._Methodology = None
        

    
    @property
    def Meaning(self):
        """
        OneElement
        """
        if self._Meaning is None:
            self._Meaning = Meaning()
        return self._Meaning
    
    @property
    def LegalReason(self):
        """
        OneElement
        """
        if self._LegalReason is None:
            self._LegalReason = LegalReason()
        return self._LegalReason
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    
    @property
    def Methodology(self):
        """
        Attribute
        """
        if self._Methodology is None:
            self._Methodology = Methodology()
        return self._Methodology
    