from flask import Flask, request
from gsuite.GSuiteComposer import *

app = Flask(__name__)


@app.route('/')
def index():
    return 'OK'


@app.route('/togsuite', methods=['POST'])
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
