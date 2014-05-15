from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing.helpers import PloneSandboxLayer
from zope.configuration import xmlconfig
from plone.testing import z2


class ActivityLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # Include ZCML
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'plone.contentrules')
        z2.installProduct(app, 'plone.app.contentrules')

        import ftw.activitystation.tests
        xmlconfig.file('configure.zcml', ftw.activitystation.tests,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.activitystation.tests:contentrule')


ACTIVITY_FIXTURE = ActivityLayer()
ACTIVITYT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ACTIVITY_FIXTURE, ),
    name="ftw.activitystation:integration")
ACTIVITY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ACTIVITY_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.activitystation:functional")
