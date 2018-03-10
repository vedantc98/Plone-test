# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.uuid.interfaces import IAttributeUUID
from zope.component.interfaces import IObjectEvent
from zope.interface import implementer


@implementer(IRuleElementData)
class DummyCondition(SimpleItem):
    element = 'dummy.condition'
    summary = 'Dummy condition'


@implementer(IRuleElementData)
class DummyAction(SimpleItem):
    element = 'dummy.action'
    summary = 'Dummy action'


@implementer(IObjectEvent)
class DummyEvent(object):

    def __init__(self, object):
        self.object = object


class DummyRule(object):

    def __init__(self, name='dummy'):
        self.__name__ = name


@implementer(IAttributeUUID)
class DummyNonArchetypesContext(object):
    pass
