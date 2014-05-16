from ftw.activitystation import _
from ftw.activitystation import activities
from ftw.activitystation import sender
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.registry.interfaces import IRegistry
from zope import schema
from zope.component import adapts
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface


class ISendAction(Interface):
    """Interface for the configurable aspects of a send action.
    """
    kind = schema.TextLine(title=_(u"Kind"),
                           description=_(u"The kind of event."),
                           required=True)


class SendAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(ISendAction, IRuleElementData)

    kind = u''

    element = 'ftw.activitystation.actions.Send'
    summary = _(u"Send activity station notification")


class SendActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, ISendAction, Interface)

    SYSTEM_KEY = 'ftw.activitystation.system_name'

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event
        self.registry = getUtility(IRegistry)

    def __call__(self):
        actor = api.user.get_current()
        activity = activities.for_event(self.event, actor)

        if activity.is_relevant():
            data = activity.get_data()
            data['kind'] = self.element.kind
            system = self.registry.get(self.SYSTEM_KEY, None)
            if system:
                data['system'] = system
            sender.SENDER.post(data)

        return True

    def error(self, obj, error):
        pass


class SendEditForm(EditForm):
    """An edit form for the send action.
    """

    form_fields = form.FormFields(ISendAction)
    label = _(u"Edit Send Action")
    description = _(u"A send action sends activities to activity station.")
    form_name = _(u"Configure Send Action")


class SendAddForm(AddForm):
    """A degenerate "add form"" for delete actions.
    """

    form_fields = form.FormFields(ISendAction)
    label = _(u"Add Send Action")
    description = _(u"A send action sends activities to activity station.")
    form_name = _(u"Configure Send Action")

    def create(self, data):
        action = SendAction()
        form.applyChanges(action, self.form_fields, data)
        return action
