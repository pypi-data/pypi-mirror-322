
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.Standard import Standard


from pyodm.model.definition import ManyElements



class Standards(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Standards
    """

    def __init__(self):
        super().__init__()
        self.set_name("Standards")
        
        self._Standard = None
        

    
    @property
    def Standard(self):
        """
        ManyElements
        """
        if self._Standard is None:
            self._Standard = Standard()
        return self._Standard
    