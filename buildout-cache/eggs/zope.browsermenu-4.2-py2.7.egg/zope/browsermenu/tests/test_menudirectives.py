##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Browser Menu Directives Tests
"""
import unittest

from zope.configuration.xmlconfig import XMLConfig
from zope.interface import Interface, implementer
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.browsermenu.interfaces import IBrowserMenu
from zope.security.interfaces import Unauthorized, Forbidden
import zope.component

import zope.security

from zope.testing import cleanup

import zope.browsermenu
from .._compat import _u


template = """<configure
   xmlns='http://namespaces.zope.org/zope'
   xmlns:browser='http://namespaces.zope.org/browser'
   i18n_domain='zope'>
   %s
   </configure>"""

class I1(Interface): pass
class I11(I1): pass
class I12(I1): pass
class I111(I11): pass


@implementer(I1)
class C1(object):
    pass

class I2(Interface): pass

@implementer(I2)
class C2(object):
    pass

@implementer(IBrowserPublisher, I111)
class TestObject(object):

    def f(self):
        pass

    def browserDefault(self, r):
        return self, ()

    def publishTraverse(self, request, name):
        if name[:1] == 'f':
            raise Forbidden(name)
        if name[:1] == 'u':
            raise Unauthorized(name)
        return self.f

class IMyLayer(Interface):
    pass

class IMySkin(IMyLayer, IDefaultBrowserLayer):
    pass


class TestPermissions(cleanup.CleanUp, unittest.TestCase):

    def setUp(self):
        super(TestPermissions, self).setUp()
        XMLConfig('meta.zcml', zope.browsermenu)()
        XMLConfig('meta.zcml', zope.security)()

    def testMenuItemsPermission(self):
        XMLConfig('tests/menus-permissions.zcml', zope.browsermenu)()

        menu = zope.component.getUtility(IBrowserMenu, 'test_id')
        # This is a bit icky, but the menu hides too much stuff from us.
        items = zope.component.getAdapters((C2(), TestRequest()),
                                           menu.getMenuItemType())
        item = list(items)[0][1]
        self.assertEqual("zope.View", item.permission)


class Test(cleanup.CleanUp, unittest.TestCase):

    def setUp(self):
        super(Test, self).setUp()
        XMLConfig('meta.zcml', zope.browsermenu)()

    def testMenusAndMenuItems(self):
        XMLConfig('tests/menus.zcml', zope.browsermenu)()

        menu = zope.browsermenu.menu.getMenu(
            'test_id', TestObject(), TestRequest())

        def d(n):
            return {'action': "a%s" % n,
                    'title':  "t%s" % n,
                    'description': _u(''),
                    'selected': '',
                    'submenu': None,
                    'icon': None,
                    'extra': None}

        self.assertEqual(menu[:-1], [d(5), d(6), d(3), d(2), d(1)])
        self.assertEqual(
            menu[-1],
            {'submenu': [{'submenu': None,
                          'description': _u(''),
                          'extra': None,
                          'selected': _u(''),
                          'action': _u('a10'),
                          'title': _u('t10'),
                          'icon': None}],
             'description': _u(''),
             'extra': None,
             'selected': _u(''),
             'action': _u(''),
             'title': _u('s1'),
             'icon': None})

        first = zope.browsermenu.menu.getFirstMenuItem(
            'test_id', TestObject(), TestRequest())

        self.assertEqual(first, d(5))

    def testMenuItemWithLayer(self):
        XMLConfig('tests/menus.zcml', zope.browsermenu)()

        menu = zope.browsermenu.menu.getMenu(
            'test_id', TestObject(), TestRequest())
        self.assertEqual(len(menu), 6)

        menu = zope.browsermenu.menu.getMenu(
            'test_id', TestObject(), TestRequest(skin=IMyLayer))
        self.assertEqual(len(menu), 2)

        menu = zope.browsermenu.menu.getMenu(
            'test_id', TestObject(), TestRequest(skin=IMySkin))
        self.assertEqual(len(menu), 8)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        unittest.makeSuite(TestPermissions),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
