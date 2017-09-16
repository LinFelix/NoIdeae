#!/usr/bin/env python
import networkx as nx

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.plotting import ColumnDataSource
from bokeh.palettes import Spectral4

class plotData(object):
    def __init__(self, data, net_graph, graph_layout, names):
        self.data = data
        self.net_graph = net_graph
        self.graph_layout = graph_layout
        self.source = ColumnDataSource(data=dict(desc=names))

    def plot_data(self, w, h):
        plot = Plot(plot_width=w, plot_height=h,
                    x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
        plot.title.text = "Graph Interaction Demonstration"

        plot.add_tools(HoverTool(tooltips=([("desc", "@desc")]), TapTool(), BoxSelectTool()))
        graph_file = os.path.join(os.getcwd(), 'data/graph')

        if not os.path.isfile(graph_file):
            graph = self.build_graph()
            with open(graph_file, 'w') as g_file:
                pickle.dump(graph, g_file)
        else:
            with open(graph_file, 'r+') as g_file:
                graph = pickle.load(g_file)

        graph_renderer = from_networkx(graph, nx.spring_layout, scale=1,
                                       center=(0, 0))
        graph_renderer.selection_policy = NodesAndLinkedEdges()
        graph_renderer.inspection_policy = EdgesAndLinkedNodes()

        plot.renderers.append(graph_renderer)
        output_file("interactive_graphs.html")
        show(plot)
