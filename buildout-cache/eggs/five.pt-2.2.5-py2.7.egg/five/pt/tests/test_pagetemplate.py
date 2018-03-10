import os

from Testing.ZopeTestCase import ZopeTestCase
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

path = os.path.dirname(__file__)


class TestPageTemplateFile(ZopeTestCase):
    def afterSetUp(self):
        from Products.Five import zcml
        import five.pt
        zcml.load_config("configure.zcml", five.pt)

    def _makeOne(self, name):
        return PageTemplateFile(os.path.join(path, name)).\
               __of__(self.app)

    def test_rr(self):
        class Prioritzed(object):
            __allow_access_to_unprotected_subobjects__ = 1

            def __init__(self, order):
                self.order = order

            def __str__(self):
                return 'P%d' % self.order

        template = self._makeOne('rr.pt')
        result = template(refs=[Prioritzed(1), Prioritzed(2)])
        self.assertTrue('P1' in result)
        self.assertTrue(result.index('P1') < result.index('P2'))

    def test_locals(self):
        template = self._makeOne('locals.pt')
        result = template()
        self.failUnless('function test' in result)
        self.failUnless('function same_type' in result)

    def test_locals_base(self):
        template = self._makeOne('locals_base.pt')
        result = template()
        self.failUnless('Application' in result)

    def test_nocall(self):
        template = self._makeOne("nocall.pt")

        def dont_call():
            raise RuntimeError()
        result = template(callable=dont_call)
        self.failUnless(repr(dont_call) in result)

    def test_exists(self):
        template = self._makeOne("exists.pt")

        def dont_call():
            raise RuntimeError()
        result = template(callable=dont_call)
        self.failUnless('ok' in result)

    def test_simple(self):
        template = self._makeOne("simple.pt")
        result = template()
        self.failUnless('Hello world!' in result)

    def test_secure(self):
        soup = '<foo></bar>'
        template = self._makeOne("secure.pt")
        from zExceptions import Unauthorized
        try:
            result = template(soup=soup)
        except Unauthorized:
            pass
        else:
            self.fail("Expected unauthorized.")

        from AccessControl.SecurityInfo import allow_module
        allow_module("cgi")
        result = template(soup=soup)
        self.failUnless('&lt;foo&gt;&lt;/bar&gt;' in result)
