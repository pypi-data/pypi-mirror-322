
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.Type import Type

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.Attribute import Attribute

from pyodm.model.cdisc.classv2.attribute.Label import Label


from pyodm.model.cdisc.classv2.element.Selection import Selection


from pyodm.model.definition import ManyElements



class Resource(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Resource
    """

    def __init__(self):
        super().__init__()
        self.set_name("Resource")
        
        self._Selection = None
        
        self._Type = None
        
        self._Name = None
        
        self._Attribute = None
        
        self._Label = None
        

    
    @property
    def Selection(self):
        """
        ManyElements
        """
        if self._Selection is None:
            self._Selection = Selection()
        return self._Selection
    
    @property
    def Type(self):
        """
        Attribute
        """
        if self._Type is None:
            self._Type = Type()
        return self._Type
    
    @property
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    
    @property
    def Attribute(self):
        """
        Attribute
        """
        if self._Attribute is None:
            self._Attribute = Attribute()
        return self._Attribute
    
    @property
    def Label(self):
        """
        Attribute
        """
        if self._Label is None:
            self._Label = Label()
        return self._Label
    