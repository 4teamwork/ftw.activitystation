from ftw.activitystation import sender
from ftw.activitystation.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from plone import api


class TestSender(object):

    def __init__(self):
        self.queue = []

    def post(self, event):
        self.queue.append(event)


class TestActivity(FunctionalTestCase):

    def setUp(self):
        super(TestActivity, self).setUp()
        sender.SENDER = self.sender = TestSender()

    def test_content_rule_triggers_activity_station_events(self):
        # create(Builder('folder'))
        parent = api.content.create(type='Folder', title='hmm',
                                    container=self.portal)

        self.assertEqual(1, len(self.sender.queue))
