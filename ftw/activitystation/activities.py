from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
from plone.uuid.interfaces import IUUID


class NullActivity(object):

    def is_relevant(self):
        return False


class AbstractActivity(object):
    def __init__(self, actor, event):
        self.actor = actor
        self.event = event
        self.obj = event.object

    def is_relevant(self):
        return True

    def get_actor_id(self):
        return self.actor.getId()

    def get_actor_name(self):
        return self.actor.getProperty("fullname") or self.actor.getId()

    def get_object_id(self):
        return IUUID(self.obj)

    def get_object_title(self):
        return self.obj.Title()

    def get_path(self):
        return "/".join(self.obj.getPhysicalPath())

    def get_url(self):
        return self.obj.absolute_url()

    def get_payload(self):
        return {
            "uuid": self.get_object_id(),
            "title": self.get_object_title(),
        }

    def get_data(self):
        return {
            "kind": self.get_kind(),
            "actor": self.get_actor_id(),
            "url": self.get_url(),
            "path": self.get_path(),
            "message": self.get_message(),
            "payload": self.get_payload(),
        }

    def get_kind(self):
        raise NotImplementedError()

    def get_message(self):
        raise NotImplementedError()


class ObjectModifiedActivity(AbstractActivity):
    def get_kind(self):
        return "bearbeitet"

    def get_message(self):
        return "{0} hat {1} bearbeitet".format(self.get_actor_name(),
                                               self.get_object_title())


class ObjectCreatedActivity(AbstractActivity):
    def get_kind(self):
        return "erstellt"

    def get_message(self):
        return "{0} hat {1} erstellt".format(self.get_actor_name(),
                                             self.get_object_title())


class ObjectDeletedActivity(AbstractActivity):

    def is_relevant(self):
        request = self.obj.REQUEST
        if getattr(request, '_activity_reported', False):
            return False
        else:
            setattr(request, '_activity_reported', True)

        info = ILinkIntegrityInfo(request)
        if not info.integrityCheckingEnabled():
            return True
        elif info.isConfirmedItem(self.obj):
            return True

        if request.URL.endswith('/sl_delete_object'):
            return True
        if request.has_key('form.submitted') and \
                request.URL.endswith('/delete_confirmation'):
            return True
        if request.URL.endswith('/folder_delete'):
            return True
        if request.has_key('form.button.Cancel'):
            return True
        return False

    def get_kind(self):
        return "entfernt"

    def get_message(self):
        return "{0} hat {1} entfernt".format(self.get_actor_name(),
                                             self.get_object_title())

    def get_url(self):
        return None


def for_event(event, actor):
    class_name = event.__class__.__name__
    clazz = mapping.get(class_name, NullActivity)
    return clazz(actor, event)


mapping = {
    "ObjectAddedEvent": ObjectCreatedActivity,
    "ObjectEditedEvent": ObjectModifiedActivity,
    "ObjectRemovedEvent": ObjectDeletedActivity,
    }
