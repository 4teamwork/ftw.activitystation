from ftw.activitystation.testing import ACTIVITY_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing.helpers import setRoles
from plone.app.testing.interfaces import TEST_USER_ID
from unittest2 import TestCase


class FunctionalTestCase(TestCase):

    layer = ACTIVITY_FUNCTIONAL_TESTING

    def setUp(self):
        super(FunctionalTestCase, self).setUp()

        self.app = self.layer['app']
        self.portal = self.layer['portal']

        self.setup_default_workflow()
        self.set_testuser_manager_role()

    def set_testuser_manager_role(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def setup_default_workflow(self):
        """Workflows are not configured by default.
        """

        wftool = api.portal.get_tool(name='portal_workflow')
        wftool.setDefaultChain('simple_publication_workflow')
