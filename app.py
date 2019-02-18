from flask import Flask, request
from gsuite.GSuiteComposer import *

import json
import pandas as pd
from numbers import Number
from collections import OrderedDict

app = Flask(__name__)

SEP = '->'
URL_PATH = 'id' + SEP + 'url'
TITLE_PATH = 'name' + SEP + 'short_label'
GENOME_PATH = 'genome_assembly'


@app.route('/')
def index():
    return 'OK'


@app.route('/togsuite', methods=['POST'])
def to_gsuite():
    gsuite = GSuite()
    data = json.loads(request.data, object_pairs_hook=OrderedDict)
    for item in data:
        createTracks(gsuite, item)

    return composeToString(gsuite)


def createTracks(gsuite, data):
        if 'fair_tracks' not in data:
            return

        columns = []
        for path in dictPaths(data['fair_tracks']):
            columns.append(path)

        result = pd.io.json.json_normalize(data['fair_tracks'], ['tracks'], columns, sep=SEP)
        result = result.to_dict('records')
        # normalize has to be run twice to unpack json in tracks list
        result = pd.io.json.json_normalize(result, sep=SEP)
        result = result.to_dict('records')

        trackNames = []
        for track in data['fair_tracks']['tracks']:
            cols = dictPaths(track)
            names = []
            for column in cols:
                names.append(SEP.join(column))
            trackNames.append(names)

        columnNames = []
        for column in columns:
            columnNames.append(SEP.join(column))

        for i, track in enumerate(result):
            # order the columns as in input json and cast numbers to string
            trackOrdered = OrderedDict()
            for col in trackNames[i]:
                if isinstance(track[col], Number):
                    trackOrdered[col] = str(track[col])
                else:
                    trackOrdered[col] = track[col]

            for col in columnNames:
                if col in track:
                    if isinstance(track[col], Number):
                        trackOrdered[col] = str(track[col])
                    else:
                        trackOrdered[col] = track[col]

            uri = trackOrdered.pop(URL_PATH, None)
            if not uri:
                continue
            gsuite.addTrack(GSuiteTrack(uri=uri, attributes=trackOrdered, title=trackOrdered[TITLE_PATH],
                                        genome=trackOrdered[GENOME_PATH]))


def dictPaths(myDict, path=[]):
    for k,v in myDict.iteritems():
        newPath = path + [k]
        if isinstance(v, dict):
            for item in dictPaths(v, newPath):
                yield item
        elif type(v) is not list:
            yield newPath


if __name__ == '__main__':
    pd.set_option('display.max_colwidth', -1)
    app.run(host='127.0.0.1')
