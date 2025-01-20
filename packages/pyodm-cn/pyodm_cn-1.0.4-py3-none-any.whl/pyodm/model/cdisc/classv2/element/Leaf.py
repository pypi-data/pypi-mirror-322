
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.ID import ID

from pyodm.model.cdisc.classv2.attribute.xlink_href import XlinkHref


from pyodm.model.cdisc.classv2.element.Title import Title


from pyodm.model.definition import ManyElements



class Leaf(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Leaf
    """

    def __init__(self):
        super().__init__()
        self.set_name("Leaf")
        
        self._Title = None
        
        self._ID = None
        
        self._xlink_href = None
        

    
    @property
    def Title(self):
        """
        ManyElements
        """
        if self._Title is None:
            self._Title = Title()
        return self._Title
    
    @property
    def ID(self):
        """
        Attribute
        """
        if self._ID is None:
            self._ID = ID()
        return self._ID
    
    @property
    def xlink_href(self):
        """
        Attribute
        """
        if self._xlink_href is None:
            self._xlink_href = XlinkHref()
        return self._xlink_href
    