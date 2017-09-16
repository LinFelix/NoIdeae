# /bin/env python3

from flask import Flask, request, render_template
from libs import reutherAPIwrapper as rw

app = Flask(__name__)


@app.route('/')
def hello_world():
    # raw = rw.ReutherAPIWrapper("HackZurichAPI", "8XtQb447")
    return render_template('index.html', channels=
    ['Disaster_Accident', 'Environment', 'Health_Medical_Pharma', 'Education', 'Business_Finance', 'Politics',
     'Social Issues', 'War_Conflict', 'Entertainment_Culture', 'Law_Crime', 'Human Interest', 'Sports',
     'Technology_Internet', 'Religion_Belief', 'Labor', 'Weather', 'Hospitality_Recreation'])


@app.route('/', methods=['POST'])
def post_choosen_channel_alias():
    print("blubb")
    list_of_chosen_tags = request.json['alias']
    pass_list_of_tags(list_of_chosen_tags)
    return "Hello world"


def pass_list_of_tags(list_of_tags):
    #  list_of_tags is a list of Strings
    pass
