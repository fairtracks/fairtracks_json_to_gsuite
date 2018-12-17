#from flask import Flask, request
from gsuite.GSuiteComposer import *

import json
import pandas as pd
from numbers import Number

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
        data = json.load(testData)
        pd.set_option('display.max_colwidth', -1)

        columns = []
        for path in dictPaths(data['fair_tracks']):
            columns.append(path)

        result = pd.io.json.json_normalize(data['fair_tracks'], ['tracks'], columns)
        result = result.to_dict('records')

        gsuite = GSuite()
        for track in result:
            #convert possible numeric values to str as gsuite requires it
            track = {k: str(v) if isinstance(v, Number) else v for k, v in track.iteritems()}
            uri = track.pop('url', None)
            if not uri:
                continue
            gsuite.addTrack(GSuiteTrack(uri=uri, attributes=track))

        print composeToString(gsuite)

        composeToFile(gsuite, './data/result')

def dictPaths(myDict, path=[]):
    for k,v in myDict.iteritems():
        newPath = path + [k]
        if type(v) is dict:
            for item in dictPaths(v, newPath):
                yield item
        elif type(v) is not list:
            yield newPath


if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    toGsuiteTmp()
