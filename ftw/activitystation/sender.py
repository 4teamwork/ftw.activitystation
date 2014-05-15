from plone.registry.interfaces import IRegistry
from urlparse import urljoin
from zope.component import getUtility
import json
import requests


class ActivityStationSender(object):

    URL_KEY = 'ftw.activitystation.url'

    def post(self, data):
        registry = getUtility(IRegistry)
        url = registry.get(self.URL_KEY, None)
        if not url:
            return

        url = urljoin(url, 'events')
        headers = {"Content-Type": "application/json"}
        requests.post(url, data=json.dumps(data), headers=headers)


SENDER = ActivityStationSender()
