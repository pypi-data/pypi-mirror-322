
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.OID import OID

from pyodm.model.cdisc.classv2.attribute.Name import Name

from pyodm.model.cdisc.classv2.attribute.DataType import DataType

from pyodm.model.cdisc.classv2.attribute.Length import Length

from pyodm.model.cdisc.classv2.attribute.DisplayFormat import DisplayFormat

from pyodm.model.cdisc.classv2.attribute.VariableSet import VariableSet

from pyodm.model.cdisc.classv2.attribute.CommentOID import CommentOID


from pyodm.model.cdisc.classv2.element.Description import Description

from pyodm.model.cdisc.classv2.element.Definition import Definition

from pyodm.model.cdisc.classv2.element.Question import Question

from pyodm.model.cdisc.classv2.element.Prompt import Prompt

from pyodm.model.cdisc.classv2.element.CRFCompletionInstructions import CRFCompletionInstructions

from pyodm.model.cdisc.classv2.element.ImplementationNotes import ImplementationNotes

from pyodm.model.cdisc.classv2.element.CDISCNotes import CDISCNotes

from pyodm.model.cdisc.classv2.element.RangeCheck import RangeCheck

from pyodm.model.cdisc.classv2.element.CodeListRef import CodeListRef

from pyodm.model.cdisc.classv2.element.ValueListRef import ValueListRef

from pyodm.model.cdisc.classv2.element.Coding import Coding

from pyodm.model.cdisc.classv2.element.Alias import Alias


from pyodm.model.definition import ManyElements



class ItemDef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemDef
    """

    def __init__(self):
        super().__init__()
        self.set_name("ItemDef")
        
        self._Description = None
        
        self._Definition = None
        
        self._Question = None
        
        self._Prompt = None
        
        self._CRFCompletionInstructions = None
        
        self._ImplementationNotes = None
        
        self._CDISCNotes = None
        
        self._RangeCheck = None
        
        self._CodeListRef = None
        
        self._ValueListRef = None
        
        self._Coding = None
        
        self._Alias = None
        
        self._OID = None
        
        self._Name = None
        
        self._DataType = None
        
        self._Length = None
        
        self._DisplayFormat = None
        
        self._VariableSet = None
        
        self._CommentOID = None
        

    
    @property
    def Description(self):
        """
        ManyElements
        """
        if self._Description is None:
            self._Description = Description()
        return self._Description
    
    @property
    def Definition(self):
        """
        OneElement
        """
        if self._Definition is None:
            self._Definition = Definition()
        return self._Definition
    
    @property
    def Question(self):
        """
        OneElement
        """
        if self._Question is None:
            self._Question = Question()
        return self._Question
    
    @property
    def Prompt(self):
        """
        OneElement
        """
        if self._Prompt is None:
            self._Prompt = Prompt()
        return self._Prompt
    
    @property
    def CRFCompletionInstructions(self):
        """
        OneElement
        """
        if self._CRFCompletionInstructions is None:
            self._CRFCompletionInstructions = CRFCompletionInstructions()
        return self._CRFCompletionInstructions
    
    @property
    def ImplementationNotes(self):
        """
        OneElement
        """
        if self._ImplementationNotes is None:
            self._ImplementationNotes = ImplementationNotes()
        return self._ImplementationNotes
    
    @property
    def CDISCNotes(self):
        """
        OneElement
        """
        if self._CDISCNotes is None:
            self._CDISCNotes = CDISCNotes()
        return self._CDISCNotes
    
    @property
    def RangeCheck(self):
        """
        ManyElements
        """
        if self._RangeCheck is None:
            self._RangeCheck = RangeCheck()
        return self._RangeCheck
    
    @property
    def CodeListRef(self):
        """
        ManyElements
        """
        if self._CodeListRef is None:
            self._CodeListRef = CodeListRef()
        return self._CodeListRef
    
    @property
    def ValueListRef(self):
        """
        ManyElements
        """
        if self._ValueListRef is None:
            self._ValueListRef = ValueListRef()
        return self._ValueListRef
    
    @property
    def Coding(self):
        """
        ManyElements
        """
        if self._Coding is None:
            self._Coding = Coding()
        return self._Coding
    
    @property
    def Alias(self):
        """
        ManyElements
        """
        if self._Alias is None:
            self._Alias = Alias()
        return self._Alias
    
    @property
    def OID(self):
        """
        Attribute
        """
        if self._OID is None:
            self._OID = OID()
        return self._OID
    
    @property
    def Name(self):
        """
        Attribute
        """
        if self._Name is None:
            self._Name = Name()
        return self._Name
    
    @property
    def DataType(self):
        """
        Attribute
        """
        if self._DataType is None:
            self._DataType = DataType()
        return self._DataType
    
    @property
    def Length(self):
        """
        Attribute
        """
        if self._Length is None:
            self._Length = Length()
        return self._Length
    
    @property
    def DisplayFormat(self):
        """
        Attribute
        """
        if self._DisplayFormat is None:
            self._DisplayFormat = DisplayFormat()
        return self._DisplayFormat
    
    @property
    def VariableSet(self):
        """
        Attribute
        """
        if self._VariableSet is None:
            self._VariableSet = VariableSet()
        return self._VariableSet
    
    @property
    def CommentOID(self):
        """
        Attribute
        """
        if self._CommentOID is None:
            self._CommentOID = CommentOID()
        return self._CommentOID
    