
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.SourceItem import SourceItem

from pyodm.model.cdisc.classv2.element.Coding import Coding


from pyodm.model.definition import OneElement



class SourceItems(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SourceItems
    """

    def __init__(self):
        super().__init__()
        self.set_name("SourceItems")
        
        self._SourceItem = None
        
        self._Coding = None
        

    
    @property
    def SourceItem(self):
        """
        ManyElements
        """
        if self._SourceItem is None:
            self._SourceItem = SourceItem()
        return self._SourceItem
    
    @property
    def Coding(self):
        """
        ManyElements
        """
        if self._Coding is None:
            self._Coding = Coding()
        return self._Coding
    