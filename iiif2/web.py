#!/usr/bin/env python
# -*-coding: utf-8 -*-

"""
    web.py
    ~~~~~~
    Utilities for creating a IIIF Image API 2.0 compliant Web Service.

    :copyright: (c) 2015 by Authors
    :license: see LICENSE for more details.
"""

import hashlib
import re
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse
from PIL import Image
from .iiif import VALID_COLOR_MODES, VALID_FILE_FMTS
from . import exc


def urihash(uri):
    """Returns a unique, short, string by md5 hashing the specified
    uri. Can be used for generating short filenames for caching a tile
    at a uri."""
    return hashlib.md5(uri.encode('utf-8')).hexdigest()


def info(uri, path, context=None, profile=None, tiles=None):
    width, height = Image.open(path).size
    return {
        '@id': uri,
        '@context': context or 'http://iiif.io/api/image/2/context.json',
        'protocol': 'http://iiif.io/api/image',
        'width': width, 'height': height,
        'profile': profile or ['http://iiif.io/api/image/2/level2.json'],
        'tiles': tiles or [{"width": 512, "scaleFactors": [1, 2, 4, 8, 16]}]
        }


class Parse(object):

    @classmethod
    def params(cls, identifier, region, size, rotation, quality, fmt):
        """Parses each param into a data structure usable as **kwargs by
        IIIF.render().

        usage:
            >>> IIIF.render(*Parse.params(
            ...     'image-service', 'abcd1234', 'full', 'full',
            ...     '0', 'default', 'jpg'))
        """
        return {
            'identifier': identifier,
            'region': cls.region(region),
            'size': cls.size(size),
            'rotation': cls.rotation(rotation),
            'quality': cls.quality(quality),
            'fmt': cls.format(fmt)
            }

    @classmethod
    def uri(cls, uri):
        """Converts a full iiif uri into its 6 constitutent
        params/components (identifier, region, size, rotation,
        quality, format) and then parses them into data structures
        usable as *args by IIIF.render()

        usage:
            >>> IIIF.render(*Parse.uri(
            ... 'http://www.example.org/image-service/abcd1234/'
            ... 'full/full/0/default.jpg'))
        """
        params = re.findall(r"[^./]+", urlparse(uri).path)[-6:]
        return cls.params(*params)

    @staticmethod
    def region(region):
        """Transform the `region` component of an IIIF url and parse it into
        iiif2 keyword arguments

        see: http://iiif.io/api/image/2.0/#region
        e.g. /{identifier}/{region}/{size}/{rotation}/{quality}.{format}
        """
        if region == 'full':
            return {'full': True}
        percent = region.startswith('pct:')
        xywh = [float(d) for d in region.lstrip('pct:').split(',')]
        dimensions = dict(zip(list('xywh'), xywh))
        if percent:
            dimensions['percent'] = percent
        return dimensions

    @staticmethod
    def size(dimensions):
        if dimensions == 'full':
            return {'full': True}

        if dimensions.startswith('pct:'):
            return {'percent': float(dimensions.lstrip('pct:')[1])}

        width_height = [int(d) if d else '' for d in dimensions.split(',')]
        return dict(zip(list('wh'), width_height))

    @staticmethod
    def rotation(degrees):
        flip = degrees.startswith('!')
        rotate = {
            'degrees': int(degrees.lstrip('!'))
            }
        if flip:
            rotate['flip'] = flip
        return rotate

    @staticmethod
    def quality(color):
        color = color.lower()
        if color not in VALID_COLOR_MODES:
            raise exc.QualityArgumentError("Invalid color scale quality")
        return {'mode': color}

    @staticmethod
    def format(fmt):
        ext = fmt.lower()
        if ext not in VALID_FILE_FMTS:
            raise exc.FormatArgumentError(
                "Invalid Tile file format. Valid options are: %s" %
                VALID_FILE_FMTS.keys())
        return {'fmt': ext}
