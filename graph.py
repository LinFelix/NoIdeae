import networkx as nx
import os
import json
import sys
import matplotlib.pyplot as plt

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from bokeh.models import ColumnDataSource, Circle, Plot, Range1d, HoverTool, TapTool, BoxSelectTool, WheelZoomTool
from bokeh.palettes import Spectral4
from bokeh.models.renderers import GraphRenderer

if __name__=='__main__':

    MIN_RELEVANCE = 0.8
    MIN_SCORE = 0.9

    datadir = sys.argv[1]

    all_entities = []
    all_relevant_topics = []
    entities_relevant_appearances = {}
    entities_relevant_topics = {}
    entities_relevant_cooccurences = {}

    for article_file in os.listdir(datadir):
        article_data = json.load(open(datadir+"/"+article_file))
        article_entities = []
        article_topics = []

        for tag in article_data.values():

            try:
                type_group = tag['_typeGroup']
            except KeyError:
                continue

            if type_group == 'entities' and tag["relevance"] >= MIN_RELEVANCE:

                entity = tag["name"]
                article_entities.append(entity)

                if entity not in all_entities:
                    all_entities.append(entity)

                    entities_relevant_appearances.update({entity: 1})
                else:
                    count = entities_relevant_appearances[entity]
                    entities_relevant_appearances.update({entity: count+1})

            if type_group == "topics" and tag["score"] >= MIN_SCORE:
                topic = tag["name"]
                article_topics.append(topic)
                if topic not in all_relevant_topics:
                    all_relevant_topics.append(topic)


        for topic in article_topics:

            for entity in article_entities:
                try:
                    topics = entities_relevant_topics[entity]
                    try:
                        count = topics[topic]
                        entities_relevant_topics[entity].update({topic: count+1})
                    except KeyError:
                        entities_relevant_topics[entity].update({topic: 1})
                except KeyError:
                    entities_relevant_topics.update({entity: {topic: 1}})


        for entity1 in article_entities:
            for entity2 in article_entities:
                if entity1 is not entity2:

                    if entity1 not in entities_relevant_cooccurences:
                        entities_relevant_cooccurences.update({entity1: {entity2: 1}})
                    else:
                        try:
                            count = entities_relevant_cooccurences[entity1][entity2]
                            entities_relevant_cooccurences[entity1].update({entity2: count+1})
                        except KeyError:
                            entities_relevant_cooccurences[entity1].update({entity2: 1})

                    if entity2 not in entities_relevant_cooccurences:
                        entities_relevant_cooccurences.update({entity2: {entity1: 1}})
                    else:
                        try:
                            count = entities_relevant_cooccurences[entity2][entity1]
                            entities_relevant_cooccurences[entity2].update({entity1: count+1})
                        except KeyError:
                            entities_relevant_cooccurences[entity2].update({entity1: 1})


    for entity, count in entities_relevant_appearances.items():
        print(entity+": {}".format(count))

    for entity, relevant_topics in entities_relevant_topics.items():
        print(entity+ ": {}".format(relevant_topics))

    for entity, relevant_cooccurences in entities_relevant_cooccurences.items():
        print(entity+ ": {}".format(relevant_cooccurences))

    print("Number of relevant entities: {}".format(len(all_entities)))
    print("Number of relevant topics: {}".format(len(all_relevant_topics)))


    map_entity_to_id = dict(zip(all_entities, range(len(all_entities))))
    map_id_to_entity = dict(zip(range(len(all_entities)), all_entities))

    dod = {}
    for entity1 in all_entities:
        id1 = map_entity_to_id[entity1]
        dod.update({id1: {}})
        try:
            for entity2, count in entities_relevant_cooccurences[entity1].items():
                id2 = map_entity_to_id[entity2]
                dod[id1].update({id2: {"weight": count}})
        except KeyError:
            continue


    G = nx.from_dict_of_dicts(dod)

    plot = Plot(plot_width=400, plot_height=400, x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))

    plot.add_tools(HoverTool(tooltips=[("entity", "@entity")]), TapTool(), BoxSelectTool(), WheelZoomTool())

    graph_renderer = from_networkx(G, nx.spring_layout, scale=2, center=(0,0))

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])

    graph_renderer.node_renderer.data_source.column_names.append("entity")
    graph_renderer.node_renderer.data_source.data.update({"entity": all_entities})

    plot.renderers.append(graph_renderer)

    output_file("networkx_graph.html")
    show(plot)