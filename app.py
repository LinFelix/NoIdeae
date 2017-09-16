# /bin/env python3

from flask import Flask, request, redirect, render_template
from libs import reutherAPIwrapper as rw
from graph import Data
app = Flask(__name__)


@app.route('/')
def hello_world():
    raw = rw.ReutherAPIWrapper("HackZurichAPI", "8XtQb447")
    return render_template('index.html', channels=raw.get_channel_list())

@app.route('/',methods=['POST'])
def post_choosen_channel_alias():
    query_topics = request.json['alias']

    data_graph = Data(query_topics)
    data_graph.build_graph()
    data_graph.draw_graph()

    return "Hello world"


def pass_list_of_tags(list_of_tags):
    #  list_of_tags is a list of Strings
    pass