
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Path import Path



from pyodm.model.definition import ManyElements



class Selection(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Selection
    """

    def __init__(self):
        super().__init__()
        self.set_name("Selection")
        
        self._Path = None
        

    
    @property
    def Path(self):
        """
        Attribute
        """
        if self._Path is None:
            self._Path = Path()
        return self._Path
    