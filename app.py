import json

from flask import Flask, request

from gsuite.GSuiteComposer import *

app = Flask(__name__)

SEP = '->'
URL_PATH = 'file_iri'
TITLE_PATH = 'label_short'
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
    if 'tracks' not in data:
        return

    trackData = OrderedDict()
    for path, value in dictPaths(data['tracks']):
        trackData[path] = value

    dataWithoutTracks = data.copy()
    dataWithoutTracks.pop('tracks')

    noTrackData = OrderedDict()
    for path, value in dictPaths(dataWithoutTracks):
        noTrackData[path] = value

    # # order the columns as in input json with track attributes first
    resultOrdered = OrderedDict()
    for col in trackData:
        if trackData[col]:
            resultOrdered[col] = trackData[col]

    for col in noTrackData:
        if noTrackData[col]:
            resultOrdered[col] = noTrackData[col]

    uri = resultOrdered.pop(URL_PATH, None)
    if not uri:
        return
    gsuite.addTrack(GSuiteTrack(uri=uri, attributes=resultOrdered, title=resultOrdered[TITLE_PATH],
                                genome=resultOrdered[GENOME_PATH]))


def dictPaths(myDict, path=[]):
    for k,v in myDict.iteritems():
        newPath = path + [k]
        if isinstance(v, dict):
            for item in dictPaths(v, newPath):
                yield item
        else:
            # track attributes should not have 'tracks->' in the attribute name
            if newPath[0] == 'tracks':
                yield SEP.join(newPath[1:]), str(v)
            else:
                if isinstance(v, list):
                    yield SEP.join(newPath), ','.join(v)
                else:
                    yield SEP.join(newPath), str(v)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


