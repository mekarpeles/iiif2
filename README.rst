iiif2
=====

.. image:: https://travis-ci.org/mekarpeles/iiif2.svg
    :target: https://travis-ci.org/mekarpeles/iiif2

An implementation of the IIIF Image API 2.0 Specification 

Installation
------------

.. code:: bash

    $ pip3 install iiif2

Usage
-----

The iiif2 library includes an image processing component called IIIF,
responsible for implementing the iiif image processing pipeline, and a
Parse utility capable of extracting iiif parameters and their data
from uris.

.. code:: python

    from iiif2 import IIIF
    from iiif2.web import Parse

You can combine the IIIF and Parse objects to create iiif 2.0 image
tiles using only:

- a iiif image 2.0 uri and
- a resolved image filepath

An image path may be provided in one of two ways. First, it can be
manually specified as a string:

.. code:: python

    from iiif2 import IIIF, web

    url = 'https://stacks.stanford.edu/image/iiif/'
          'ff139pd0160%252FK90113-43/full/full/0/default.jpg'

    # a web server can return a rendered tile directly
    # without ever saving tile to disk. Works on read-only fs:
    tile = IIIF.render('images/file.jpg', *web.Parse(url)) 

    # if we want, we can save tile (e.g. for caching)
    tile.save('cache/%s' % web.urihash(url))


Example Web Service
-------------------

An entire IIIF Web Service written in Flask in ~30 lines of code is
provided in the examples/ folder.

.. code:: python

    import os.path
    from flask import Flask, request, jsonify, send_file
    from iiif2 import IIIF, web

    PATH = os.path.dirname(os.path.realpath(__file__))
    app = Flask(__name__)


    @app.route('/<identifier>/info.json')
    def info(identifier):
	  return jsonify(web.info(request.url_root, identifier))


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
