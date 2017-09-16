#!/usr/bin/env python
from __future__ import print_function, division
import json
import glob


class Article:
    def __init__(self, file_name, threshold=0.6):
        with open(file_name) as file:
            self.data = json.load(file)
        self.entities = {}
        self.important_entities = {}
        self.socialTags = {}
        self.topics = {}

        self.parse(threshold)

    def parse(self, threshold=0.6):
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
                    print(value)
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

    def get_freq_entities(self, n_threshold):
        freq_ent = {}
        for ent, (rel, n_count) in self.entities.items():
            if n_count >= n_threshold:
                freq_ent[ent] = n_count

        return freq_ent


class ArticleData:
    def __init__(self):
        self.rel_entities = {}
        self.freq_entities = {}
        self.data = []

    def parse_data(self, folder_path, threshold, n_threshold):
        for file in glob.glob(folder_path + "*.json"):
            self.data.append(Article(file, threshold))
            rel_entities = self.data[-1].get_rel_entities()
            freq_entities = self.data[-1].get_freq_entities(n_threshold)
            for entity in rel_entities:
                if entity in self.rel_entities:
                    self.rel_entities[entity].update(rel_entities)
                else:
                    self.rel_entities[entity] = set(rel_entities)

            for entity in freq_entities:
                if entity in self.freq_entities:
                    self.freq_entities[entity].update(freq_entities)
                else:
                    self.freq_entities[entity] = set(freq_entities)





