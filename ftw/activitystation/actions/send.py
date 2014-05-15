from ftw.activitystation import activities
from ftw.activitystation import sender
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from zope import schema
from zope.component import adapts
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

    element = 'plone.actions.Send'
    summary = _(u"Send activity station notification")


class SendActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, ISendAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        actor = api.user.get_current()
        activity = activities.for_event(self.event, actor)

        if activity.is_relevant():
            data = activity.get_data()
            data['kind'] = self.element.kind
            sender.SENDER.post(data)

        return True

    def error(self, obj, error):
        pass


class SendEditForm(EditForm):
    """An edit form for the send action.
    """

    form_fields = form.FormFields(ISendAction)
    label = _(u"Edit Send Action")
    description = _(u"A send action send events.")
    form_name = _(u"Configure element")


class SendAddForm(AddForm):
    """A degenerate "add form"" for delete actions.
    """

    form_fields = form.FormFields(ISendAction)
    label = _(u"Add Send Action")
    description = _(u"A send action send events.")
    form_name = _(u"Configure element")

    def create(self, data):
        action = SendAction()
        form.applyChanges(action, self.form_fields, data)
        return action
