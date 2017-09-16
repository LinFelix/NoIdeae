#!/usr/bin/env python
from __future__ import print_function, division
import json
import glob


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
