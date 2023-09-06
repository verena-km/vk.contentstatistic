# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import vk.contentstatistic


class VkContentstatisticLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=vk.contentstatistic)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "vk.contentstatistic:default")


VK_CONTENTSTATISTIC_FIXTURE = VkContentstatisticLayer()


VK_CONTENTSTATISTIC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VK_CONTENTSTATISTIC_FIXTURE,),
    name="VkContentstatisticLayer:IntegrationTesting",
)


VK_CONTENTSTATISTIC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VK_CONTENTSTATISTIC_FIXTURE,),
    name="VkContentstatisticLayer:FunctionalTesting",
)


VK_CONTENTSTATISTIC_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        VK_CONTENTSTATISTIC_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="VkContentstatisticLayer:AcceptanceTesting",
)
