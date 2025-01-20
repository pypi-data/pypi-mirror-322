
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.WhereClauseOID import WhereClauseOID



from pyodm.model.definition import ManyElements



class WhereClauseRef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/WhereClauseRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("WhereClauseRef")
        
        self._WhereClauseOID = None
        

    
    @property
    def WhereClauseOID(self):
        """
        Attribute
        """
        if self._WhereClauseOID is None:
            self._WhereClauseOID = WhereClauseOID()
        return self._WhereClauseOID
    