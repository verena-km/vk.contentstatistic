# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from vk.contentstatistic.testing import (  # noqa: E501
    VK_CONTENTSTATISTIC_INTEGRATION_TESTING,
)

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that vk.contentstatistic is properly installed."""

    layer = VK_CONTENTSTATISTIC_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if vk.contentstatistic is installed."""
        self.assertTrue(self.installer.is_product_installed("vk.contentstatistic"))

    def test_browserlayer(self):
        """Test that IVkContentstatisticLayer is registered."""
        from plone.browserlayer import utils
        from vk.contentstatistic.interfaces import IVkContentstatisticLayer

        self.assertIn(IVkContentstatisticLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = VK_CONTENTSTATISTIC_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("vk.contentstatistic")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if vk.contentstatistic is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("vk.contentstatistic"))

    def test_browserlayer_removed(self):
        """Test that IVkContentstatisticLayer is removed."""
        from plone.browserlayer import utils
        from vk.contentstatistic.interfaces import IVkContentstatisticLayer

        self.assertNotIn(IVkContentstatisticLayer, utils.registered_layers())
