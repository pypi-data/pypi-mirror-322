
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.UserOID import UserOID



from pyodm.model.definition import OneElement



class UserRef(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/UserRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("UserRef")
        
        self._UserOID = None
        

    
    @property
    def UserOID(self):
        """
        Attribute
        """
        if self._UserOID is None:
            self._UserOID = UserOID()
        return self._UserOID
    