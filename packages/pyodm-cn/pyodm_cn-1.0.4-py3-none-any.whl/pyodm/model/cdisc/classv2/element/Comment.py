
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.SponsorOrSite import SponsorOrSite


from pyodm.model.cdisc.classv2.element.TranslatedText import TranslatedText


from pyodm.model.definition import OneElement



class Comment(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Comment
    """

    def __init__(self):
        super().__init__()
        self.set_name("Comment")
        
        self._TranslatedText = None
        
        self._SponsorOrSite = None
        

    
    @property
    def TranslatedText(self):
        """
        ManyElements
        """
        if self._TranslatedText is None:
            self._TranslatedText = TranslatedText()
        return self._TranslatedText
    
    @property
    def SponsorOrSite(self):
        """
        Attribute
        """
        if self._SponsorOrSite is None:
            self._SponsorOrSite = SponsorOrSite()
        return self._SponsorOrSite
    