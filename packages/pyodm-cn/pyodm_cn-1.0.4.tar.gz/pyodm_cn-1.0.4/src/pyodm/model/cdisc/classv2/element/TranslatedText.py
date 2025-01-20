
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.xml_lang import XmlLang

from pyodm.model.cdisc.classv2.attribute.Type import Type



from pyodm.model.definition import ManyElements



class TranslatedText(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/TranslatedText
    """

    def __init__(self):
        super().__init__()
        self.set_name("TranslatedText")
        
        self._xml_lang = None
        
        self._Type = None
        

    
    @property
    def xml_lang(self):
        """
        Attribute
        """
        if self._xml_lang is None:
            self._xml_lang = XmlLang()
        return self._xml_lang
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    