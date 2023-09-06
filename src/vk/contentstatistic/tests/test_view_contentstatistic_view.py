# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from vk.contentstatistic.testing import VK_CONTENTSTATISTIC_FUNCTIONAL_TESTING
from vk.contentstatistic.testing import VK_CONTENTSTATISTIC_INTEGRATION_TESTING
from vk.contentstatistic.views.contentstatistic_view import IContentstatisticView
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = VK_CONTENTSTATISTIC_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "Document", "front-page")

    def test_content_statistic_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST), name="content-statistic"
        )
        self.assertTrue(IContentstatisticView.providedBy(view))

    def test_content_statistic_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST),
                name="content-statistic",
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IContentstatisticView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = VK_CONTENTSTATISTIC_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
