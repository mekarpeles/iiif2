#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    tests.test_packaging
    ~~~~~~~~~~~~~~~~~~~~

    This module tests the pypc packaging pipeline

    :copyright: (c) 2015 by Mek.
    :license: see LICENSE for more details.
"""

import os
import unittest
from PIL import Image
from iiif2 import IIIF
from iiif2 import Parse

# Expected Tile dimensions
WIDTH = 1000
HEIGHT = 1095

# IIIF Params
IDENTIFIER = 'ff139pd0160%252FK90113-43'
REGION = {'x': 1400, 'y': 1200, 'w': 2500, 'h': 1075}
SIZE = {'w': WIDTH, 'h': ''}
ROTATION = 0
QUALITY = 'default'
FORMAT = 'jpg'

# What Parse.uri(TEST_URI) should return
PARAMS = {
    'identifier': IDENTIFIER,
    "region": REGION,
    "size": SIZE,
    'rotation': {'degrees': ROTATION},
    'quality': {'mode': QUALITY},
    'fmt': {'fmt': FORMAT}
}

DOMAIN = '{scheme}://{server}/{prefix}'.format(
    scheme='http', server='stacks.stanford.edu', prefix='image/iiif')
URI_PARAMS = '{identifier}/{region}/{size}/{rotation}/{quality}.{fmt}'\
    .format(identifier=IDENTIFIER,
            region='{x},{y},{w},{h}'.format(**REGION),
            size='{w},{h}'.format(**SIZE),
            rotation=ROTATION,
            quality=QUALITY,
            fmt=FORMAT)
TEST_URI = '%s/%s' % (DOMAIN, URI_PARAMS)
TEST_IMG_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir, 'examples', 'flask-iiif', 'images'
        )
    )
TEST_IMG_PATH = os.path.join(TEST_IMG_DIR, IDENTIFIER + '.jpg')
EXPECTED_MIME = "image/jpeg"


class TestIIIF(unittest.TestCase):

    def test_parse(self):
        params = Parse.uri(TEST_URI)
        self.assertTrue(params == PARAMS, "Param matching failed. "
                        "%s v. %s" % (params, PARAMS))

    def test_render(self):
        """Does not parse, uses PARAMS dict to render tile"""
        with IIIF.render(TEST_IMG_PATH, **Parse.uri(TEST_URI)) as t1:
            with IIIF.render(TEST_IMG_PATH, **PARAMS) as t2:
                self.assertTrue(t1.contents() == t2.contents(),
                                "Parsing uri behaving differently "
                                "than PARAMS")
                im = Image.open(t1)
                self.assertTrue(im.size == (WIDTH, HEIGHT),
                                "Tile is the wrong dimensions: "
                                "Expected %s got %s."
                                % ((WIDTH, HEIGHT), im.size))
                im.close()
