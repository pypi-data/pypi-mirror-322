
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.SignatureOID import SignatureOID



from pyodm.model.definition import OneElement



class SignatureRef(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SignatureRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("SignatureRef")
        
        self._SignatureOID = None
        

    
    @property
    def SignatureOID(self):
        """
        Attribute
        """
        if self._SignatureOID is None:
            self._SignatureOID = SignatureOID()
        return self._SignatureOID
    