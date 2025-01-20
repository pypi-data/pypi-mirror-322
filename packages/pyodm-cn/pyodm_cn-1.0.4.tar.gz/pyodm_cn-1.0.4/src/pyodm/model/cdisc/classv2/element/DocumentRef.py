
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.leafID import LeafID


from pyodm.model.cdisc.classv2.element.PDFPageRef import PDFPageRef


from pyodm.model.definition import ManyElements



class DocumentRef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/DocumentRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("DocumentRef")
        
        self._PDFPageRef = None
        
        self._LeafID = None
        

    
    @property
    def PDFPageRef(self):
        """
        ManyElements
        """
        if self._PDFPageRef is None:
            self._PDFPageRef = PDFPageRef()
        return self._PDFPageRef
    
    @property
    def LeafID(self):
        """
        Attribute
        """
        if self._LeafID is None:
            self._LeafID = LeafID()
        return self._LeafID
    