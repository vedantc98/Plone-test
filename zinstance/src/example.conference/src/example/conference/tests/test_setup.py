# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from example.conference.testing import EXAMPLE_CONFERENCE_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that example.conference is properly installed."""

    layer = EXAMPLE_CONFERENCE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if example.conference is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'example.conference'))

    def test_browserlayer(self):
        """Test that IExampleConferenceLayer is registered."""
        from example.conference.interfaces import (
            IExampleConferenceLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IExampleConferenceLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = EXAMPLE_CONFERENCE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['example.conference'])

    def test_product_uninstalled(self):
        """Test if example.conference is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'example.conference'))

    def test_browserlayer_removed(self):
        """Test that IExampleConferenceLayer is removed."""
        from example.conference.interfaces import \
            IExampleConferenceLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           IExampleConferenceLayer,
           utils.registered_layers())
