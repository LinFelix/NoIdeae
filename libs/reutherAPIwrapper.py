#! /bin/env python3

import requests
import xml.etree.ElementTree as ET


USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"
AUTH_URL = "https://commerce.reuters.com/rmd/rest/xml/"
SERVICE_URL = "http://rmb.reuters.com/rmd/rest/xml/"


class ReutherAPIWrapper:

    def __init__(self, username=USERNAME, password=PASSWORD):
        _token_response = ET.fromstring(requests.get(
            '{}login?username={}&password={}'
            .format(AUTH_URL, username, password)).text)
        if _token_response.tag != 'authToken':
            pass
        else:
            self._authToken = _token_response.text
        self.available_channels = {}

    def get_channel_list(self):  # without categories
        _channel_list_response = requests.get(
            '{}/channels?&token={}'.format(SERVICE_URL, self._authToken))
        _channel_list_tree_root = ET.fromstring(_channel_list_response.text)
        for channel_information in _channel_list_tree_root:
            try:
                self.available_channels[channel_information[0].text] =\
                    channel_information[1].text
            except:
                # print(channel_information.text)
                pass  # channel_information faulty

    def get_items_meta(self, channel_alias):
        _items_respons =\
            requests.get('{}/items?channel={}&token={}'
                         .format(SERVICE_URL, channel_alias, self._authToken))
        itemslist = []
        for result in ET.fromstring(_items_respons.text):
            pass


if __name__ == '__main__':
    reutherAPIWrapper = ReutherAPIWrapper("HackZurichAPI", "8XtQb447")
    reutherAPIWrapper.get_channel_list()