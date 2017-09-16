#!/usr/bin/env python
from __future__ import print_function, division
import requests
from urllib import urlencode
from collections import defaultdict
import json
import glob

from xml.etree.ElementTree import fromstring

USERNAME = "HackZurichAPI"
PASSWORD = "8XtQb447"
AUTH_URL = "https://commerce.reuters.com/rmd/rest/xml/"
SERVICE_URL = "http://rmb.reuters.com/rmd/rest/xml/"


class ReutersData:
    def __init__(self, username=USERNAME, password=PASSWORD):
        self.auth_token = None
        self._authenticate(username, password)
        self.channels = {}

    def _authenticate(self, username, password):
        params = urlencode({'username': USERNAME,
                            'password': PASSWORD})
        resp = requests.get(AUTH_URL + 'login', params=params)
        if not resp.ok:
            print('Something went wrong!')
        resp_txt = fromstring(resp.text)
        if resp_txt.tag == 'authToken':
            token = resp_txt.text
            self.auth_token = token

    def get_data(self, method, args={}):
        root_url = SERVICE_URL
        url = root_url + method
        args['token'] = self.auth_token
        params = urlencode(args)
        resp = requests.get(url, params=params)
        etree = fromstring(resp.text)
        return ReutersData.etree_to_dict(etree)

    def get_channels(self):
        return self.channels['availableChannels'].keys()

    def get_channel_aliases(self):
        channels = [ele for ele in self.channels['availableChannels']['channelInformation']]
        aliases = [ele['alias'] for ele in channels]
        # print(len(channels))
        # print(channels[0])
        # print(channels[0]['category']['@description'])
        # print(channels[0]['category']['@id'])
        return aliases

    def request_channels(self, task='channels'):
        channels_dict = self.get_data(task)
        self.channels = channels_dict

    def request_items(self, channel, task='items'):
        items_dict = self.get_data(task, {'channel': channel})
        return items_dict

    @staticmethod
    def etree_to_dict(t):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(ReutersData.etree_to_dict, children):
                for k, v in dc.iteritems():
                    dd[k].append(v)
            d = {
                t.tag: {k: v[0] if len(v) == 1 else v for k, v in
                        dd.iteritems()}
            }
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                    d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d


class Article:
    def __init__(self, file_name):
        with open(file_name) as file:
            self.data = json.load(file)
        self.entities = {}
        self.important_entities = {}
        self.socialTags = {}
        self.topics = {}

        self.parse()

    def parse(self, threshold=0.5):
        for value in self.data.values():
            try:
                type_group = value['_typeGroup']
                if type_group == 'entities':
                    entity = value['name']
                    relevance = value['relevance']
                    num = len(value['instances'])
                    self.entities[entity] = (relevance, num)
                    if relevance > threshold:
                        self.important_entities[entity] = (relevance, num)
                elif type_group == 'socialTag':
                    name = value['name']
                    importance = value['importance']
                    self.socialTags[name] = importance
                elif type_group == 'topics':
                    self.topics[value['name']] = value['score']
            except KeyError:
                pass

    def get_entities(self):
        return self.entities.keys()

    def get_rel_entities(self):
        return self.important_entities.keys()


class CsvData:
    def __init__(self):
        self.entities = {}
        self.data = []

    def parse_data(self, folder_path):
        for file in glob.glob(folder_path + "*.json"):
            self.data.append(Article(file))
            for entity in self.data[-1].get_rel_entities():
                self.entities[entity]
            self.entities.update(self.data.get_entities())




def demo():
    data = Article('sampletext.json')
    data.get_entities()


if __name__ == '__main__':
    demo()