
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.Description import Description


from pyodm.model.definition import ManyElements



class IntercurrentEvent(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/IntercurrentEvent
    """

    def __init__(self):
        super().__init__()
        self.set_name("IntercurrentEvent")
        
        self._Description = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    