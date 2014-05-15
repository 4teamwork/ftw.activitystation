from ftw.activitystation import sender
from ftw.activitystation.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing.interfaces import TEST_USER_ID
from plone.uuid.interfaces import IUUID


class TestSender(object):

    def __init__(self):
        self.queue = []

    def post(self, event):
        self.queue.append(event)

    def __len__(self):
        return len(self.queue)

    def pop(self):
        return self.queue.pop()


class TestActivity(FunctionalTestCase):

    def setUp(self):
        super(TestActivity, self).setUp()
        sender.SENDER = self.sender = TestSender()

    def test_content_rule_triggers_activity_station_events(self):
        folder = create(Builder('folder').titled('Testfolder'))

        self.assertEqual(1, len(self.sender))
        activity = self.sender.pop()

        self.assertIn('payload', activity)
        payload = activity['payload']
        self.assertEqual('Testfolder', payload['title'])
        self.assertEqual(IUUID(folder), payload['uuid'])

        self.assertEqual('test_event', activity['kind'])
        self.assertEqual(TEST_USER_ID, activity['actor'])
        self.assertEqual(folder.absolute_url(), activity['url'])
        self.assertEqual("/".join(folder.getPhysicalPath()),
                         activity['path'])
        self.assertIn('message', activity)
