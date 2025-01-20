
import pyodm.model.meta.cdisc_odm_entity as Meta



from pyodm.model.definition import ManyElements



class PDFPageRef(ManyElements,Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/PDFPageRef
    """

    def __init__(self):
        super().__init__()
        self.set_name("PDFPageRef")
        

    