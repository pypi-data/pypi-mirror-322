
import pyodm.model.meta.cdisc_odm_entity as Meta


from pyodm.model.cdisc.classv2.element.TranslatedText import TranslatedText


from pyodm.model.definition import ManyElements



class Description(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Description
    """

    def __init__(self):
        super().__init__()
        self.set_name("Description")
        
        self._TranslatedText = None
        

    
    @property
    def TranslatedText(self):
        """
        ManyElements
        """
        if self._TranslatedText is None:
            self._TranslatedText = TranslatedText()
        return self._TranslatedText
    