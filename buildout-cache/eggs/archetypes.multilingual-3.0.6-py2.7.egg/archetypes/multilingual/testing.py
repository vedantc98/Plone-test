# -*- coding: utf-8 -*-
from OFS.Folder import Folder
from Testing import ZopeTestCase as ztc
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.multilingual.testing import PLONE_APP_MULTILINGUAL_FIXTURE
from plone.app.contenttypes.testing import (
    PLONE_APP_CONTENTTYPES_FIXTURE,
    PLONE_APP_CONTENTTYPES_MIGRATION_FIXTURE
)
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig

import doctest
import transaction


class ArchetypesMultilingualLayer(PloneSandboxLayer):

    defaultBases = (
        PLONE_APP_CONTENTTYPES_MIGRATION_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # import Products.ATContentTypes
        # self.loadZCML(package=Products.ATContentTypes)

        # z2.installProduct(app, 'Products.Archetypes')
        # z2.installProduct(app, 'Products.ATContentTypes')

        import archetypes.multilingual

        xmlconfig.file('testing.zcml', archetypes.multilingual,
                       context=configurationContext)

        # if not hasattr(app, 'temp_folder'):
        #     tf = Folder('temp_folder')
        #     app._setObject('temp_folder', tf)
        #     transaction.commit()

        # ztc.utils.setupCoreSessions(app)

    def setUpPloneSite(self, portal):
        # install Products.ATContentTypes manually if profile is available
        # (this is only needed for Plone >= 5)
        # profiles = [x['id'] for x in portal.portal_setup.listProfileInfo()]
        applyProfile(portal, 'plone.app.multilingual:default')
        applyProfile(portal, 'archetypes.multilingual:default')

ARCHETYPESMULTILINGUAL_FIXTURE = ArchetypesMultilingualLayer()

ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ARCHETYPESMULTILINGUAL_FIXTURE,),
    name="archetypes.multilingual:Integration")
ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ARCHETYPESMULTILINGUAL_FIXTURE,),
    name="archetypes.multilingual:Functional")

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
