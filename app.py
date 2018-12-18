#from flask import Flask, request
from gsuite.GSuiteComposer import *

import json
import pandas as pd
from numbers import Number
from collections import OrderedDict

#app = Flask(__name__)


#@app.route('/')
def index():
    return 'OK'


#"@app.route('/togsuite', methods=['POST'])
def to_gsuite():
    gsuite = GSuite()
    attributes = request.json['attributes']
    datasets = request.json['datasets']
    for dataset in datasets:
        standard_content = dict((k, str(v)) for k, v in dataset['fair'].iteritems() if v)
        if 'uri' in standard_content:
            uri = standard_content.pop('uri', None)
            gsuite.addTrack(GSuiteTrack(uri=uri, attributes=standard_content))
    return composeToString(gsuite)

def toGsuiteTmp():
    with open('./data/fair_tracks_example2.json') as testData:
        data = json.load(testData, object_pairs_hook=OrderedDict)
        pd.set_option('display.max_colwidth', -1)

        columns = []
        for path in dictPaths(data['fair_tracks']):
            columns.append(path)

        result = pd.io.json.json_normalize(data['fair_tracks'], ['tracks'], columns, sep='->')
        result = result.to_dict('records')

        trackNames = []
        for track in data['fair_tracks']['tracks']:
            cols = dictPaths(track)
            names = []
            for column in cols:
                names.append("->".join(column))
            trackNames.append(names)

        columnNames = []
        for column in columns:
            columnNames.append("->".join(column))

        gsuite = GSuite()
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

            uri = trackOrdered.pop('url', None)
            if not uri:
                continue
            gsuite.addTrack(GSuiteTrack(uri=uri, attributes=trackOrdered, title=trackOrdered['short_label'],
                                        genome=trackOrdered['genome_assembly']))

        print composeToString(gsuite)

        composeToFile(gsuite, './data/result')

def dictPaths(myDict, path=[]):
    for k,v in myDict.iteritems():
        newPath = path + [k]
        if isinstance(v, dict):
            for item in dictPaths(v, newPath):
                yield item
        elif type(v) is not list:
            yield newPath


if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    toGsuiteTmp()
