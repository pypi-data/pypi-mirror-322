
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.Source import Source


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.SourceItems import SourceItems

from pyodm.model.cdisc.classv2.element.Coding import Coding

from pyodm.model.cdisc.classv2.element.DocumentRef import DocumentRef


from pyodm.model.definition import ManyElements



class Origin(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Origin
    """

    def __init__(self):
        super().__init__()
        self.set_name("Origin")
        
        self._Description = None
        
        self._SourceItems = None
        
        self._Coding = None
        
        self._DocumentRef = None
        
        self._Type = None
        
        self._Source = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def SourceItems(self):
        """
        OneElement
        """
        if self._SourceItems is None:
            self._SourceItems = SourceItems()
        return self._SourceItems
    
    @property
    def Coding(self):
        """
        ManyElements
        """
        if self._Coding is None:
            self._Coding = Coding()
        return self._Coding
    
    @property
    def DocumentRef(self):
        """
        ManyElements
        """
        if self._DocumentRef is None:
            self._DocumentRef = DocumentRef()
        return self._DocumentRef
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def Source(self):
        """
        Attribute
        """
        if self._Source is None:
            self._Source = Source()
        return self._Source
    