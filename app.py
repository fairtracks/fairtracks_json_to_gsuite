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
        gsuite.addTrack(GSuiteTrack(uri='http://test.com/file.tar.gz', attributes=dataset['standardContent']))
    return composeToString(gsuite)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
