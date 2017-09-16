# -*- coding: utf-8 -*-
from unidecode import unidecode
import json
import os

class Persons(object):
    def __init__(self):
        self.id = []
        self.data = []

    def add_data(self, key, data):
        self.id.append(key)
        self.data.append(data)

    def print_data(self):
        for idx, id in enumerate(self.id):
            print(self.data[idx])

    def query(self, info):
        response = []
        for data in self.data:
            for key in data.keys():
                if info in data[key]:
                    response.append(data)
        return response


class Parser(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.informations = Persons()

    def _decode_list(self, data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = self._decode_list(item)
            elif isinstance(item, dict):
                item = self._decode_dict(item)
            elif isinstance(item, int):
                item = str(item)
            elif isinstance(item, float):
                item = str(item)
            rv.append(item)
        return rv

    def _decode_dict(self, data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = self._decode_list(value)
            elif isinstance(value, dict):
                value = self._decode_dict(value)
            elif isinstance(value, int):
                value = str(value)
            elif isinstance(value, float):
                value = str(value)
            rv[key] = value
        return rv

    def load_data(self, file_path):
        with open(os.path.join(self.data_path, file_path)) as data_file:
            data = json.load(data_file, object_hook=self._decode_dict)
        for key in data.keys():
            self.informations.add_data(key, data[key])

    def query(self, info):
        return self.informations.query(info)


if __name__=='__main__':
    data_path = 'data/'
    parser = Parser(data_path)

    parser.load_data('sampletext.json')
    print(parser.query('European Union'))
