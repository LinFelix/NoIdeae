# /bin/env python3

from flask import Flask, request, redirect, render_template
from libs import reutherAPIwrapper as rw
app = Flask(__name__)

@app.route('/')
def hello_world():
    raw = rw.ReutherAPIWrapper("HackZurichAPI", "8XtQb447")
    return render_template('index.html', channels=raw.get_channel_list())
