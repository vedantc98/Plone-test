# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFPlone.interfaces.defaultpage import IDefaultPage
from Products.CMFPlone.defaultpage import get_default_page
from Products.CMFPlone.defaultpage import is_default_page
from Products.Five.browser import BrowserView
from zope.interface import implementer


@implementer(IDefaultPage)
class DefaultPage(BrowserView):

    def isDefaultPage(self, obj):
        return is_default_page(aq_inner(self.context), obj)

    def getDefaultPage(self):
        return get_default_page(aq_inner(self.context))
