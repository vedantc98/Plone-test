# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from example.conference.interfaces import IProgram
from example.conference.testing import EXAMPLE_CONFERENCE_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ProgramIntegrationTest(unittest.TestCase):

    layer = EXAMPLE_CONFERENCE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Program')
        schema = fti.lookupSchema()
        self.assertEqual(IProgram, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Program')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Program')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IProgram.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='Program',
            id='Program',
        )
        self.assertTrue(IProgram.providedBy(obj))
