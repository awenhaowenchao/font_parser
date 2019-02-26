#!/usr/bin/python
#coding=utf-8

import json
from flask import Flask, request
from werkzeug.wrappers import Response
from parser.maoyan_font_parser import *
from config.setting import *

app = Flask(__name__)

parser_dict = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Font Parser Home</h1>'

@app.route('/parse', methods=['POST'])
def parse():
    if 'application/json' not in request.content_type:
        return 'Content type %s not supported' % request.content_type
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        channel = json_data.get('channel')
        font_url = json_data.get('font_url')
        data = json_data.get('data')
        parser = get_channel_parser(channel)
        font = parser.load(font_url)
        result = font.normalize(data)
        if parser and parser != None:
            resp = Response(response=result, status=200, content_type='application/json')
            return resp
        else:
            resp = Response(response='', status=200, content_type='application/json')
            return resp
def init_channel_parser():
    for subclass in FontParser.__subclasses__():
        subClazz = subclass()
        parser_dict[subClazz.name] = subClazz

def get_channel_parser(channel):
    return parser_dict.get(channel)

if __name__ == '__main__':
    init_channel_parser()
    app.run(debug=debug, port=port)