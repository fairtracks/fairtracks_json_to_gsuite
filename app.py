from flask import Flask, request
from gsuite.GSuiteComposer import *

app = Flask(__name__)


@app.route('/')
def index():
    return 'OK'


@app.route('/togsuite', methods=['POST'])
def to_gsuite():
    gsuite = GSuite()
    for dataset in request.json:
        standard_content = dict((k, str(v)) for k, v in dataset['standardContent'].iteritems() if v)
        gsuite.addTrack(GSuiteTrack(uri='http://test.com/file.tar.gz', attributes=standard_content))
    return composeToString(gsuite)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
