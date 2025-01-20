from pathlib import Path

from lxml import etree
import copy
import os

from jinja2 import FileSystemLoader, Environment


class GenerateCdiscModel:
    def __init__(self, xsd_files: list):
        self.xsd_files = xsd_files
        self.attributeGroups = dict()
        self.complexTypes = dict()
        self.cdiscElements = dict()
        self.groups = dict()

    def parse(self):
        for xsd_file in self.xsd_files:
            xsd_tree = etree.parse(xsd_file)
            root = xsd_tree.getroot()
            for element in root:
                if not isinstance(element.tag, str): continue
                name = etree.QName(element.tag).localname
                if name == "attributeGroup":
                    self.attributeGroup(element)
                if name == "complexType":
                    self.complexType(element)
                if name == "element":
                    self.cdisc_element(element)
                if name == 'group':
                    self.group(element)
            # print(element)

    def group(self, element):
        self.groups[element.attrib.get("name")] = dict(elements=[])
        for x in element:
            if not isinstance(x.tag, str): continue
            if etree.QName(x.tag).localname == "sequence":
                for y in x:
                    if not isinstance(y.tag, str): continue
                    if etree.QName(y.tag).localname == "element":
                        ref = y.attrib.get("ref").replace(":", "_")
                        cls_type = "model.OneElement()" if y.attrib.get("maxOccurs") is None else "model.ManyElements()"
                        self.groups[element.attrib.get("name")]["elements"].append(
                            dict(name=ref, cls_type=cls_type))

    def cdisc_element(self, element):
        self.cdiscElements[element.attrib.get("name")] = element.attrib.get("type")

    def attributeGroup(self, element):
        self.attributeGroups[element.attrib.get("name")] = dict()
        for attribute in element:
            if not isinstance(attribute.tag, str): continue
            if etree.QName(attribute.tag).localname == "attribute":
                name = attribute.attrib.get("name") or attribute.attrib.get("ref").replace(":", "_")
                self.attributeGroups[element.attrib.get("name")].update({
                    name: "model.Attribute()"})

    def complexType(self, element):
        """
        临时的解析代码
        :param element:
        :type element:
        :return:
        :rtype:
        """
        self.complexTypes[element.attrib.get("name")] = dict(elements=[], attributes=[], elementGroup=[])
        for x in element:
            if not isinstance(x.tag, str): continue
            if etree.QName(x.tag).localname == "sequence":
                for y in x:
                    if not isinstance(y.tag, str): continue
                    if etree.QName(y.tag).localname == "element":
                        ref = y.attrib.get("ref").replace(":", "_")
                        cls_type = "model.OneElement()" if y.attrib.get("maxOccurs") is None else "model.ManyElements()"
                        self.complexTypes[element.attrib.get("name")]["elements"].append(
                            dict(name=ref, cls_type=cls_type))
                    if etree.QName(y.tag).localname == "group":
                        ref = y.attrib.get("ref").replace(":", "_")
                        self.complexTypes[element.attrib.get("name")]["elementGroup"].append(ref)
            if etree.QName(x.tag).localname == "attributeGroup":
                self.complexTypes[element.attrib.get("name")]["attributes"].append(
                    x.attrib.get("ref").replace(":", "_"))
            if etree.QName(x.tag).localname == "simpleContent":
                for y in x:
                    if not isinstance(y.tag, str): continue
                    if etree.QName(y.tag).localname == "extension":
                        for z in y:
                            if not isinstance(z.tag, str): continue
                            if etree.QName(z.tag).localname == "attributeGroup":
                                if not isinstance(z.tag, str): continue
                                self.complexTypes[element.attrib.get("name")]["attributes"].append(
                                    z.attrib.get("ref").replace(":", "_"))

    def cdisc(self):
        results = {}
        for name, complex_type in self.cdiscElements.items():
            results[name] = {"elements": copy.deepcopy(self.complexTypes[complex_type].get("elements")),
                             "attributes": {}}
            for groupName in self.complexTypes[complex_type].get("elementGroup"):
                if self.groups.get(groupName) is None: continue
                for element in self.groups[groupName].get("elements"):
                    results[name]["elements"].append(element)
            for ref in self.complexTypes[complex_type].get("attributes"):
                attrib = self.attributeGroups.get(ref)
                if attrib is not None:
                    results[name]["attributes"].update(attrib)
        return results

    def create_attribute(self, cdisc):
        attributes = set()

        for e in cdisc.values():
            for a in e.get("attributes"):
                attributes.add(a)

        file_loader = FileSystemLoader('./')
        env = Environment(loader=file_loader)
        template = env.get_template("template/attribute.template")

        attribute_path = Path("out_put").joinpath("attribute")
        if not attribute_path.exists():
            attribute_path.mkdir(parents=True)

        for attribute in attributes:
            output = template.render(className=self.className(attribute), attributeName=attribute)
            # with open(os.path.join('out_put', f'{cdiscName}.py'), "w", encoding="UTF-8") as f:
            with open(attribute_path.joinpath(f'{attribute}.py'), "w", encoding="UTF-8") as f:
                f.write(output)

    def className(self, name: str):
        return "".join([e[0].upper() + e[1:] for e in name.split("_")])

    def create_element(self, cdisc):
        element_types = dict()
        attribute_path = Path("out_put").joinpath("element")
        file_loader = FileSystemLoader('./')
        env = Environment(loader=file_loader)
        template = env.get_template("template/element.template")
        if not attribute_path.exists():
            attribute_path.mkdir(parents=True)
        for name, attrs in cdisc.items():
            for e in attrs.get("elements"):
                """
                处理场景
                Value
                在 ItemData 中是 ManyElements
                在 Query 中是 OneElement
                但是ManyElements 比 OneElements 更为通用，所以如果出现矛盾的情况，统一处理为ManyElements
                """
                if element_types.get(e.get("name")) is None or element_types[e.get("name")] != "ManyElements":
                    element_types[e.get("name")] = "ManyElements" if "ManyElements" in e.get("cls_type") else "OneElement"

        for name, attrs in cdisc.items():
            class_name = name
            if class_name == "Value":
                print("")
            parent_element = element_types.get(class_name)
            parent_class = ",".join([parent_element, "Meta.CdiscODMEntity"]) if parent_element else "Meta.CdiscODMEntity"
            element_class = element_types.get(class_name)
            import_attribute_class = dict()
            import_element_class = dict()
            instances = dict()
            for e in attrs.get("elements"):
                if e.get("name") != class_name:
                    import_element_class[e.get("name")] = e.get("name")
                instances[e.get("name")] = dict(Description=element_types[e.get("name")], Class=e.get("name"))
            for e in attrs.get("attributes").keys():
                import_attribute_class[e] = self.className(e)
                instances[e] = dict(Description="Attribute", Class=self.className(e))
            output = template.render(className=class_name, parentClass=parent_class, elementClass=element_class,
                                     importAttributeClass=import_attribute_class,
                                     importElementClass=import_element_class,
                                     instances=instances)

            with open(attribute_path.joinpath(f'{class_name}.py'), "w", encoding="UTF-8") as f:
                f.write(output)

    def gen(self):
        self.parse()
        cdisc = self.cdisc()
        self.create_attribute(cdisc=cdisc)
        self.create_element(cdisc=cdisc)




if __name__ == '__main__':

    xsd_files = [
            "D:\\github\\pyodm\\src\\pyodm\\model\\v2\\resources\\schema\\ODM-admindata.xsd",
            "D:\\github\\pyodm\\src\\pyodm\\model\\v2\\resources\\schema\\ODM-clinicaldata.xsd",
            "D:\\github\\pyodm\\src\\pyodm\\model\\v2\\resources\\schema\\ODM-protocol.xsd",
            "D:\\github\\pyodm\\src\\pyodm\\model\\v2\\resources\\schema\\ODM-study.xsd",
            "D:\\github\\pyodm\\src\\pyodm\\model\\v2\\resources\\schema\\ODM-referencedata.xsd",
            "D:\\github\\pyodm\\src\\pyodm\\model\\v2\\resources\\schema\\ODM-foundation.xsd"
    ]
    g = GenerateCdiscModel(xsd_files)
    g.gen()


