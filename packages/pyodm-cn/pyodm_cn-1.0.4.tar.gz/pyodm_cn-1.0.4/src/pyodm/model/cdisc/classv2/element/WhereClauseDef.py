
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID


from pyodm.model.cdisc.classv2.element.RangeCheck import RangeCheck


from pyodm.model.definition import ManyElements



class WhereClauseDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/WhereClauseDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("WhereClauseDef")
        
        self._RangeCheck = None
        
        self._OID = None
        
        self._CommentOID = None
        

    
    @property
    def RangeCheck(self):
        """
        ManyElements
        """
        if self._RangeCheck is None:
            self._RangeCheck = RangeCheck()
        return self._RangeCheck
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    
    @property
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    