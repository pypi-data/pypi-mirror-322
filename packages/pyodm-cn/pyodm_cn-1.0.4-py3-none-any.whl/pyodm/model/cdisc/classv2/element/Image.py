
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.ImageFileName import ImageFileName

from pyodm.model.cdisc.classv2.attribute.href import Href

from pyodm.model.cdisc.classv2.attribute.MimeType import MimeType



from pyodm.model.definition import OneElement



class Image(OneElement,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Image
    """

    def __init__(self):
        super().__init__()
        self.set_name("Image")
        
        self._ImageFileName = None
        
        self._href = None
        
        self._MimeType = None
        

    
    @property
    def ImageFileName(self):
        """
        Attribute
        """
        if self._ImageFileName is None:
            self._ImageFileName = ImageFileName()
        return self._ImageFileName
    
    @property
    def href(self):
        """
        Attribute
        """
        if self._href is None:
            self._href = Href()
        return self._href
    
    @property
    def MimeType(self):
        """
        Attribute
        """
        if self._MimeType is None:
            self._MimeType = MimeType()
        return self._MimeType
    