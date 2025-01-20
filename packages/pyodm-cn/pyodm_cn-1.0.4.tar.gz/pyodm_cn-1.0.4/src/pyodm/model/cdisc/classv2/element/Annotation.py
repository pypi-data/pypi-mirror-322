
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.model.cdisc.classv2.attribute.SeqNum import SeqNum

from pyodm.model.cdisc.classv2.attribute.TransactionType import TransactionType

from pyodm.model.cdisc.classv2.attribute.ID import ID


from pyodm.model.cdisc.classv2.element.Comment import Comment

from pyodm.model.cdisc.classv2.element.Coding import Coding

from pyodm.model.cdisc.classv2.element.Flag import Flag


from pyodm.model.definition import ManyElements



class Annotation(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Annotation
    """

    def __init__(self):
        super().__init__()
        self.set_name("Annotation")
        
        self._Comment = None
        
        self._Coding = None
        
        self._Flag = None
        
        self._SeqNum = None
        
        self._TransactionType = None
        
        self._ID = None
        

    
    @property
    def Comment(self):
        """
        OneElement
        """
        if self._Comment is None:
            self._Comment = Comment()
        return self._Comment
    
    @property
    def Coding(self):
        """
        ManyElements
        """
        if self._Coding is None:
            self._Coding = Coding()
        return self._Coding
    
    @property
    def Flag(self):
        """
        ManyElements
        """
        if self._Flag is None:
            self._Flag = Flag()
        return self._Flag
    
    @property
    def SeqNum(self):
        """
        Attribute
        """
        if self._SeqNum is None:
            self._SeqNum = SeqNum()
        return self._SeqNum
    
    @property
    def TransactionType(self):
        """
        Attribute
        """
        if self._TransactionType is None:
            self._TransactionType = TransactionType()
        return self._TransactionType
    
    @property
    def ID(self):
        """
        Attribute
        """
        if self._ID is None:
            self._ID = ID()
        return self._ID
    