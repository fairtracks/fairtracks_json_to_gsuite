#from flask import Flask, request
from gsuite.GSuiteComposer import *

import json
import pandas as pd

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
        #print data

        print '-------'
        pd.set_option('display.max_colwidth', -1)
        columns = []
        for key, value in data['fair_tracks'].iteritems():
            if type(value) is dict:
                for key2 in value.keys():
                    columns.append([key, key2])

        result = pd.io.json.json_normalize(data['fair_tracks'], ['tracks'], columns)

        with open('./data/result', 'w') as resultfile:
            resultfile.write(result.to_string())

        result = result.to_dict('records')
        gsuite = GSuite()

        for track in result:
            track = {k: str(v) if isinstance(v, int) else v for k, v in track.iteritems()}
            uri = track.pop('url', None)
            if not uri:
                continue
            gsuite.addTrack(GSuiteTrack(uri=uri, attributes=track))

        print composeToString(gsuite)



if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    toGsuiteTmp()
