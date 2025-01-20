from lxml import etree

from pyodm.core.support.abstract_xml_data_reader import AbstractXMLDataReader
from pyodm.factory.cdisc_registry import CdiscRegistry
from pyodm.model.definition import OneElement, ManyElements
import pyodm.model.meta.cdisc_odm_entity as Meta
from pyodm.utils.etree_utils import EtreeUtils


class XMLV2DataReader(AbstractXMLDataReader):
    def __init__(self, registry: CdiscRegistry):
        super().__init__(registry)

    def _parse(self, element, cdisc_name):
        cdisc_node = self._new_cdisc_node(cdisc_name)
        cdisc_node.set_name(cdisc_name)
        # 处理属性节点
        self._set_attribute(element, cdisc_node)
        # 处理文本节点
        self._set_text(element, cdisc_node)
        for sub_element in element:
            if isinstance(sub_element, etree._Comment): continue  # 忽略注释
            sub_cdisc_name = EtreeUtils.localname(sub_element)
            # 获取 子节点 实例
            sub_cdisc_node = self._sub_cdisc_node(cdisc_node, sub_cdisc_name)
            # 处理类型为 OneElement的Element的对象
            self._one_element(cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name)
            # 处理类型为 ManyElements的Element的对象
            self._many_element(cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name)
            # 处理类型为 只为CdiscODMEntity的Element的对象
            self._entity(cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name)
        return cdisc_node

    def _entity(self, cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name):
        if isinstance(sub_cdisc_node, Meta.CdiscODMEntity) and not isinstance(sub_cdisc_node, OneElement) and not isinstance(sub_cdisc_node, ManyElements):
            entity = self._parse(sub_element, sub_cdisc_name)
            entity.set_name(sub_cdisc_name)
            if sub_cdisc_name == "SubjectData":
                print("")
            setattr(cdisc_node, f"_{sub_cdisc_name}", entity)

    def _one_element(self, cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name):
        if isinstance(sub_cdisc_node, OneElement):
            one_element = self._parse(sub_element, sub_cdisc_name)
            one_element.set_name(sub_cdisc_name)

            setattr(cdisc_node, f"_{sub_cdisc_name}", one_element)

    def _many_element(self, cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name):
        if isinstance(sub_cdisc_node, ManyElements):
            element = self._parse(sub_element, sub_cdisc_name)
            if getattr(cdisc_node, f"_{sub_cdisc_name}") is None:
                setattr(cdisc_node, f"_{sub_cdisc_name}", element)
            else:
                getattr(cdisc_node, sub_cdisc_name) << element