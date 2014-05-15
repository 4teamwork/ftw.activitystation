import requests
import json


class ActivityStationSender(object):

    def post(self, data):
        url = 'http://activity.dev/events'
        headers = {"Content-Type": "application/json"}
        requests.post(url, data=json.dumps(data), headers=headers)


SENDER = ActivityStationSender()
