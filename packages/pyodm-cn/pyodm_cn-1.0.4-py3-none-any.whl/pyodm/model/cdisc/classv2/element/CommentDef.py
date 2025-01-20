
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.DocumentRef import DocumentRef


from pyodm.model.definition import ManyElements



class CommentDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/CommentDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("CommentDef")
        
        self._Description = None
        
        self._DocumentRef = None
        
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
    def DocumentRef(self):
        """
        ManyElements
        """
        if self._DocumentRef is None:
            self._DocumentRef = DocumentRef()
        return self._DocumentRef
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    