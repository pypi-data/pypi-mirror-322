import os

from pyodm.core.source.path_source import PathSource

from pyodm.core.xml.reader.data.xml_v2_data_reader import XMLV2DataReader
from pyodm.factory.abstract_cdisc_xml_factory import AbstractCdiscXMLFactory

import pyodm.model.cdisc.classv2.element as Element
from pyodm.model import odm_xsd_description


class CdiscV2Factory(AbstractCdiscXMLFactory):

    def default_description_files(self) -> list:
        return odm_xsd_description()

    def __init__(self, data_file: PathSource, xsd_files: list = None):
        """
        :param data_file:  数据文件路径
        :type data_file: pathlib.Path
        :param xsd_files: XSD配置文件路径, 默认使用内置的 ODM 配置
        :type xsd_files: list[pathlib.Path]
        """
        super().__init__(data_file, xsd_files)

    def data_reader(self) -> XMLV2DataReader:
        """
        指定了解析 ODM XML Data 的数据方式
        :return:
        :rtype:
        """
        return XMLV2DataReader(self)

    def clazz_reader(self):
        """
        没有用动态加载的原因
        主要是为了避免如果以后需要用pyinstall打包的话,引用的第三包里如果动态加载,执行的话无法执行
        格式定义为 Class名:类型名的原因
        因为 Definition Attributes和 Element 都有
        :return:
        :rtype:
        """
        self.registry_cdisc('AbsoluteTimingConstraint', Element.AbsoluteTimingConstraint)
        self.registry_cdisc('Address', Element.Address)
        self.registry_cdisc('AdminData', Element.AdminData)
        self.registry_cdisc('Alias', Element.Alias)
        self.registry_cdisc('AnnotatedCRF', Element.AnnotatedCRF)
        self.registry_cdisc('Annotation', Element.Annotation)
        self.registry_cdisc('Arm', Element.Arm)
        self.registry_cdisc('Association', Element.Association)
        self.registry_cdisc('AuditRecord', Element.AuditRecord)
        self.registry_cdisc('Branching', Element.Branching)
        self.registry_cdisc('CDISCNotes', Element.CDISCNotes)
        self.registry_cdisc('CheckValue', Element.CheckValue)
        self.registry_cdisc('City', Element.City)
        self.registry_cdisc('Class', Element.Class)
        self.registry_cdisc('ClinicalData', Element.ClinicalData)
        self.registry_cdisc('Code', Element.Code)
        self.registry_cdisc('CodeList', Element.CodeList)
        self.registry_cdisc('CodeListItem', Element.CodeListItem)
        self.registry_cdisc('CodeListRef', Element.CodeListRef)
        self.registry_cdisc('Coding', Element.Coding)
        self.registry_cdisc('Comment', Element.Comment)
        self.registry_cdisc('CommentDef', Element.CommentDef)
        self.registry_cdisc('ConditionDef', Element.ConditionDef)
        self.registry_cdisc('Country', Element.Country)
        self.registry_cdisc('CRFCompletionInstructions', Element.CRFCompletionInstructions)
        self.registry_cdisc('Criterion', Element.Criterion)
        self.registry_cdisc('DateTimeStamp', Element.DateTimeStamp)
        self.registry_cdisc('Decode', Element.Decode)
        self.registry_cdisc('DefaultTransition', Element.DefaultTransition)
        self.registry_cdisc('Definition', Element.Definition)
        self.registry_cdisc('Description', Element.Description)
        self.registry_cdisc('DocumentRef', Element.DocumentRef)
        self.registry_cdisc('DurationTimingConstraint', Element.DurationTimingConstraint)
        self.registry_cdisc('Epoch', Element.Epoch)
        self.registry_cdisc('ErrorMessage', Element.ErrorMessage)
        self.registry_cdisc('ExclusionCriteria', Element.ExclusionCriteria)
        self.registry_cdisc('ExternalCodeLib', Element.ExternalCodeLib)
        self.registry_cdisc('FamilyName', Element.FamilyName)
        self.registry_cdisc('Flag', Element.Flag)
        self.registry_cdisc('FlagType', Element.FlagType)
        self.registry_cdisc('FlagValue', Element.FlagValue)
        self.registry_cdisc('FormalExpression', Element.FormalExpression)
        self.registry_cdisc('FullName', Element.FullName)
        self.registry_cdisc('GeoPosition', Element.GeoPosition)
        self.registry_cdisc('GivenName', Element.GivenName)
        self.registry_cdisc('HouseNumber', Element.HouseNumber)
        self.registry_cdisc('Image', Element.Image)
        self.registry_cdisc('ImplementationNotes', Element.ImplementationNotes)
        self.registry_cdisc('Include', Element.Include)
        self.registry_cdisc('InclusionCriteria', Element.InclusionCriteria)
        self.registry_cdisc('InclusionExclusionCriteria', Element.InclusionExclusionCriteria)
        self.registry_cdisc('IntercurrentEvent', Element.IntercurrentEvent)
        self.registry_cdisc('InvestigatorRef', Element.InvestigatorRef)
        self.registry_cdisc('ItemData', Element.ItemData)
        self.registry_cdisc('ItemDef', Element.ItemDef)
        self.registry_cdisc('ItemGroupData', Element.ItemGroupData)
        self.registry_cdisc('ItemGroupDef', Element.ItemGroupDef)
        self.registry_cdisc('ItemGroupRef', Element.ItemGroupRef)
        self.registry_cdisc('ItemRef', Element.ItemRef)
        self.registry_cdisc('KeySet', Element.KeySet)
        self.registry_cdisc('Leaf', Element.Leaf)
        self.registry_cdisc('LegalReason', Element.LegalReason)
        self.registry_cdisc('Location', Element.Location)
        self.registry_cdisc('LocationRef', Element.LocationRef)
        self.registry_cdisc('Meaning', Element.Meaning)
        self.registry_cdisc('MetaDataVersion', Element.MetaDataVersion)
        self.registry_cdisc('MetaDataVersionRef', Element.MetaDataVersionRef)
        self.registry_cdisc('MethodDef', Element.MethodDef)
        self.registry_cdisc('MethodSignature', Element.MethodSignature)
        self.registry_cdisc('ODM', Element.ODM)
        self.registry_cdisc('Organization', Element.Organization)
        self.registry_cdisc('Origin', Element.Origin)
        self.registry_cdisc('OtherText', Element.OtherText)
        self.registry_cdisc('Parameter', Element.Parameter)
        self.registry_cdisc('ParameterValue', Element.ParameterValue)
        self.registry_cdisc('PDFPageRef', Element.PDFPageRef)
        self.registry_cdisc('PostalCode', Element.PostalCode)
        self.registry_cdisc('Prefix', Element.Prefix)
        self.registry_cdisc('Prompt', Element.Prompt)
        self.registry_cdisc('Protocol', Element.Protocol)
        self.registry_cdisc('Query', Element.Query)
        self.registry_cdisc('Question', Element.Question)
        self.registry_cdisc('RangeCheck', Element.RangeCheck)
        self.registry_cdisc('ReasonForChange', Element.ReasonForChange)
        self.registry_cdisc('ReferenceData', Element.ReferenceData)
        self.registry_cdisc('RelativeTimingConstraint', Element.RelativeTimingConstraint)
        self.registry_cdisc('Resource', Element.Resource)
        self.registry_cdisc('ReturnValue', Element.ReturnValue)
        self.registry_cdisc('Selection', Element.Selection)
        self.registry_cdisc('Signature', Element.Signature)
        self.registry_cdisc('SignatureDef', Element.SignatureDef)
        self.registry_cdisc('SignatureRef', Element.SignatureRef)
        self.registry_cdisc('SiteRef', Element.SiteRef)
        self.registry_cdisc('SourceID', Element.SourceID)
        self.registry_cdisc('SourceItem', Element.SourceItem)
        self.registry_cdisc('SourceItems', Element.SourceItems)
        self.registry_cdisc('Standard', Element.Standard)
        self.registry_cdisc('Standards', Element.Standards)
        self.registry_cdisc('StateProv', Element.StateProv)
        self.registry_cdisc('StreetName', Element.StreetName)
        self.registry_cdisc('Study', Element.Study)
        self.registry_cdisc('StudyEndPoint', Element.StudyEndPoint)
        self.registry_cdisc('StudyEndPointRef', Element.StudyEndPointRef)
        self.registry_cdisc('StudyEndPoints', Element.StudyEndPoints)
        self.registry_cdisc('StudyEstimand', Element.StudyEstimand)
        self.registry_cdisc('StudyEstimands', Element.StudyEstimands)
        self.registry_cdisc('StudyEventData', Element.StudyEventData)
        self.registry_cdisc('StudyEventDef', Element.StudyEventDef)
        self.registry_cdisc('StudyEventGroupDef', Element.StudyEventGroupDef)
        self.registry_cdisc('StudyEventGroupRef', Element.StudyEventGroupRef)
        self.registry_cdisc('StudyEventRef', Element.StudyEventRef)
        self.registry_cdisc('StudyIndication', Element.StudyIndication)
        self.registry_cdisc('StudyIndications', Element.StudyIndications)
        self.registry_cdisc('StudyIntervention', Element.StudyIntervention)
        self.registry_cdisc('StudyInterventionRef', Element.StudyInterventionRef)
        self.registry_cdisc('StudyInterventions', Element.StudyInterventions)
        self.registry_cdisc('StudyObjective', Element.StudyObjective)
        self.registry_cdisc('StudyObjectives', Element.StudyObjectives)
        self.registry_cdisc('StudyParameter', Element.StudyParameter)
        self.registry_cdisc('StudyStructure', Element.StudyStructure)
        self.registry_cdisc('StudySummary', Element.StudySummary)
        self.registry_cdisc('StudyTargetPopulation', Element.StudyTargetPopulation)
        self.registry_cdisc('StudyTargetPopulationRef', Element.StudyTargetPopulationRef)
        self.registry_cdisc('StudyTiming', Element.StudyTiming)
        self.registry_cdisc('StudyTimings', Element.StudyTimings)
        self.registry_cdisc('SubClass', Element.SubClass)
        self.registry_cdisc('SubjectData', Element.SubjectData)
        self.registry_cdisc('Suffix', Element.Suffix)
        self.registry_cdisc('SummaryMeasure', Element.SummaryMeasure)
        self.registry_cdisc('SupplementalDoc', Element.SupplementalDoc)
        self.registry_cdisc('TargetTransition', Element.TargetTransition)
        self.registry_cdisc('Telecom', Element.Telecom)
        self.registry_cdisc('Title', Element.Title)
        self.registry_cdisc('Transition', Element.Transition)
        self.registry_cdisc('TransitionTimingConstraint', Element.TransitionTimingConstraint)
        self.registry_cdisc('TranslatedText', Element.TranslatedText)
        self.registry_cdisc('TrialPhase', Element.TrialPhase)
        self.registry_cdisc('User', Element.User)
        self.registry_cdisc('UserName', Element.UserName)
        self.registry_cdisc('UserRef', Element.UserRef)
        self.registry_cdisc('Value', Element.Value)
        self.registry_cdisc('ValueListDef', Element.ValueListDef)
        self.registry_cdisc('ValueListRef', Element.ValueListRef)
        self.registry_cdisc('WhereClauseDef', Element.WhereClauseDef)
        self.registry_cdisc('WhereClauseRef', Element.WhereClauseRef)
        self.registry_cdisc('WorkflowDef', Element.WorkflowDef)
        self.registry_cdisc('WorkflowEnd', Element.WorkflowEnd)
        self.registry_cdisc('WorkflowRef', Element.WorkflowRef)
        self.registry_cdisc('WorkflowStart', Element.WorkflowStart)


if __name__ == '__main__':

    for f in os.listdir("D:\\github\\pyodm\\src\\pyodm\\model\\cdisc\\classv2\\element"):
        name = f.replace(".py", "")
        print(f"self.registry_cdisc('{name}:element', Element.{name})")
        # print(f"from pyodm.model.cdisc.classv2.element.{name} import {name}")
