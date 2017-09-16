#!/usr/bin/env python
from __future__ import print_function, division
import json
from itertools import combinations
import glob
import networkx as nx
import numpy as np
from bokeh.models import (Plot, Range1d, MultiLine, Circle, HoverTool,
                          TapTool, BoxSelectTool)




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
                    name = value['name']
                    importance = value['importance']
                    self.socialTags[name] = importance
                elif type_group == 'topics':
                    self.topics[value['name']] = value['score']
            except KeyError:
                pass

    def get_entities(self):
        return self.entities.keys()

    def get_relevance(self, entity):
        return self.entities[entity][0]

    def get_rel_prod(self, ent_1, ent_2):
        if ent_1 in self.important_entities.keys() and ent_2 in \
                self.important_entities.keys():
            return self.get_relevance(ent_1) * self.get_relevance(ent_2)
        else:
            return None

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
        self.entities = set([])
        self.data = []

    def parse_data(self, folder_path, threshold, n_threshold):
        for file in glob.glob(folder_path + "cl1*.json"):
            self.data.append(Article(file, threshold))
            self.entities.update(self.data[-1].entities.keys())

    def get_relevancy(self):
        ent_copy = list(self.entities)
        relevances = {}
        for ent_1, ent_2 in combinations(ent_copy, 2):
            for art in self.data:
                key = tuple([ent_1, ent_2])
                prod = art.get_rel_prod(ent_1, ent_2)
                if prod is None:
                    continue
                if key not in relevances:
                    relevances[key] = [art.get_rel_prod(ent_1, ent_2)]
                else:
                    relevances[key].append(art.get_rel_prod(ent_1, ent_2))
        return relevances

    def build_graph(self):
        relevances = self.get_relevancy()
        print(relevances)
        graph = nx.Graph()
        for ele in relevances:
            n1 = ele[0]
            n2 = ele[1]
            relevancy = np.mean(relevances[ele]) * len(relevances[ele])
            graph.add_edge(n1, n2, weight=relevancy)
        return graph

    def draw_graph(self):







