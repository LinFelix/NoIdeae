#! /bin/env python3

import requests
import xml.etree.ElementTree as ET

"""



"""


USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"
AUTH_URL = "https://commerce.reuters.com/rmd/rest/xml/"
SERVICE_URL_XML = "http://rmb.reuters.com/rmd/rest/xml/"
SERVICE_URL = "http://rmb.reuters.com/rmd/rest/json/"


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
        #items_meta_list =
        #for items in items_meta.json():
        #    items_meta_list[items] = items_meta.json()[items]
        #return items_meta_list

    def get_item_content(self, item):
        return requests.get('{}item?id={}&token={}'.format(SERVICE_URL, item['id'], self._authToken)).json()

    def throw_out_link_list(self, mylist):
        return list(filter(lambda x: x['headline'] != 'OUSWDM Link List', mylist))

    def has_text(self, item):
        return item['productlabel'] == 'text'

if __name__ == '__main__':
    reutherAPIWrapper = ReutherAPIWrapper("HackZurichAPI", "8XtQb447")
    channel_list = reutherAPIWrapper.get_channel_list()
    items_list = reutherAPIWrapper.throw_out_link_list(reutherAPIWrapper.get_items_meta(list(channel_list.values())[0]))
    for i in range(200):
        content = reutherAPIWrapper.get_item_content(items_list[i])
        if reutherAPIWrapper.has_text(content):
            print(content['body_xhtml'])
    # printing headlines
    #for i in items_list:
    #    print(i['headline'])



    #for i in items_list:
    #    print(i.headline)
    #    if i.headline == 'en':
    #        reutherAPIWrapper.get_item_content(i)

    #reutherAPIWrapper.get_item_content(items_list[0])
