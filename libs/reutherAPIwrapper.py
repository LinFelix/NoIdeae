#! /bin/env python3

import requests
import xml.etree.ElementTree as ET
import os.path

"""
How to use this script?

look in the main part down below


"""


USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"
AUTH_URL = "https://commerce.reuters.com/rmd/rest/xml/"
SERVICE_URL_XML = "http://rmb.reuters.com/rmd/rest/xml/"
SERVICE_URL = "http://rmb.reuters.com/rmd/rest/json/"


class ReutherAPIWrapper:

    def __init__(self, username=USERNAME, password=PASSWORD):
        #  get an access token and store it
        _token_response = ET.fromstring(requests.get(
            '{}login?username={}&password={}'
            .format(AUTH_URL, username, password)).text)
        if _token_response.tag != 'authToken':
            pass
        else:
            self._authToken = _token_response.text
        self.available_channels = {}

    def get_channel_list(self):  # without categories
        """
        gets all available channels
        :return: a dict with {<channel-name> : <channel-alias>}
        """
        _channel_list_response = requests.get(
            '{}/channels?&token={}'.format(SERVICE_URL_XML, self._authToken))
        _channel_list_tree_root = ET.fromstring(_channel_list_response.text)
        for channel_information in _channel_list_tree_root:
            try:
                self.available_channels[channel_information[0].text] =\
                    channel_information[1].text
            except:
                pass  # channel_information faulty
        return self.available_channels

    def get_items_meta(self, channel_alias):
        return requests.get('{}items?channel={}&token={}'.format(SERVICE_URL, channel_alias, self._authToken)).json()['results']

    def get_item_content(self, item):
        return requests.get('{}item?id={}&token={}'.format(SERVICE_URL, item['id'], self._authToken)).json()

    def get_items_meta_without_link_list(self, channel_alias):
        return list(filter(lambda x: x['headline'] != 'OUSWDM Link List', self.get_items_meta(channel_alias)))

    def has_text(self, item):
        return item['productlabel'] == 'text'

    def get_channel_aliasis(self):
        return list(self.get_channel_list().values())


def save_all_text(new_path):
    if os.path.exists(new_path):
        print("not going to overwrite files")
    else:
        os.mkdir(new_path)
        count = 0
        raw = ReutherAPIWrapper("HackZurichAPI", "8XtQb447")  # instantiate and gain access token
        channels = raw.get_channel_aliasis()  # get a list of channels
        for channel in channels:
            items_list = raw.get_items_meta_without_link_list(channel)
            for items in items_list:
                content = raw.get_item_content(items)
                if raw.has_text(content):
                    text = content["body_xhtml"]
                    with open(new_path + '/' + str(count) + ".txt", 'w') as f:
                        f.write(text)
                    count += 1


if __name__ == '__main__':
    raw = ReutherAPIWrapper("HackZurichAPI", "8XtQb447")  # instantiate and gain access token
    channels = raw.get_channel_aliasis()  # get a list of channels
    for channel in channels:
        items_list = raw.get_items_meta_without_link_list(channel)
        for items in items_list:
            content = raw.get_item_content(items)
            if raw.has_text(content):
                print(content["body_xhtml"])
