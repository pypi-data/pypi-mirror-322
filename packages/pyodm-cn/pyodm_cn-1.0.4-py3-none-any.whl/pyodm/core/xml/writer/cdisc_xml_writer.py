import pathlib

from lxml import etree

import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta

from pyodm.exceptions import XmlWriterException
from pyodm.model.definition import ManyElements, Attribute, OneElement

class CdiscXmlWriter:
    """
    ODM 对象导出为 XML 文件
    """
    """
       ODM 对象导出为 XML 文件
       """

    def __init__(self, cdisc, out_put: pathlib.Path):
        self.cdisc = cdisc
        self.out_put = out_put

    def iscdisc(self, unknown) -> bool:
        return isinstance(unknown, Meta.CdiscODMEntity) or \
               isinstance(unknown, Model.Attribute) or \
               isinstance(unknown, Model.OneElement) or \
               isinstance(unknown, Model.ManyElements)

    def write(self):

        if not isinstance(self.cdisc, Meta.CdiscODMEntity):
            raise XmlWriterException("cdisc should instance of CdiscODMEntity")
        element = self._gen_element(cdisc=self.cdisc, parent_element=None)

        dump_tree = etree.ElementTree(element=element)
        dump_tree.write(self.out_put, pretty_print=True, encoding="utf-8")

    def _gen_element(self, cdisc, parent_element):
        element = etree.Element(cdisc.get_name()) if parent_element is None else etree.SubElement(parent_element,
                                                                                                  cdisc.get_name())
        for name, cdisc_instance in vars(cdisc).items():
            if not self.iscdisc(cdisc_instance): continue
            if isinstance(cdisc_instance, Model.OneElement) and isinstance(cdisc_instance, Meta.CdiscODMEntity):
                self._one_element(cdisc_one_element=cdisc_instance, parent_element=element)
            elif isinstance(cdisc_instance, Model.ManyElements) and isinstance(cdisc_instance, Meta.CdiscODMEntity):
                self._many_element(cdisc_many_element=cdisc_instance, parent_element=element)
            elif isinstance(cdisc_instance, Model.Attribute):
                self._attribute(cdisc_attribute=cdisc_instance, parent_element=element)
            elif isinstance(cdisc_instance, Meta.CdiscODMEntity):
                self._entity(cdisc_entity=cdisc_instance, parent_element=element)
        return element

    def _entity(self, cdisc_entity: Meta.CdiscODMEntity, parent_element):
        self._gen_element(cdisc=cdisc_entity, parent_element=parent_element)

    def _attribute(self, cdisc_attribute: Attribute, parent_element):
        if not cdisc_attribute.no_use():
            parent_element.attrib[cdisc_attribute.get_name()] = str(cdisc_attribute.get_value())

    def _one_element(self, cdisc_one_element: OneElement, parent_element):
        element = self._gen_element(cdisc_one_element, parent_element=parent_element)
        if not cdisc_one_element.is_blank():
            element.text = cdisc_one_element.get_value()

    def _many_element(self, cdisc_many_element: ManyElements, parent_element):
        # element = self._gen_element(cdisc_many_element, parent_element=parent_element)
        for e in cdisc_many_element.array:
            element = self._gen_element(e, parent_element)
            if not e.is_blank():
                element.text = e.get_value()
