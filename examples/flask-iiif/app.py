import os.path
from flask import Flask, request, jsonify, send_file
from iiif2 import IIIF, web

PATH = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)


@app.route('/<identifier>/info.json')
def info(identifier):
    return jsonify(web.info(request.url, resolve(identifier), identifier))


@app.route('/<identifier>/<region>/<size>/<rotation>/<quality>.<fmt>')
def iiif(**kwargs):
    params = web.Parse.params(**kwargs)
    path = resolve(params.get('identifier'))
    with IIIF.render(path, **params) as tile:
        return send_file(tile, mimetype=tile.mime)


def resolve(identifier):
    """Resolves a iiif identifier to the resource's path on disk.
    This method is specific to this server's architecture.
    """
    return os.path.join(PATH, 'images', '%s.jpg' % identifier)


if __name__ == "__main__":
    app.run(debug=True)
