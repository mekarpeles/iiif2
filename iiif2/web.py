#!/usr/bin/env python
# -*-coding: utf-8 -*-

"""
    web.py
    ~~~~~~
    Utilities for creating a IIIF Image API 2.0 compliant Web Service.

    :copyright: (c) 2015 by Authors
    :license: see LICENSE for more details.
"""


class Parse(object):

    @staticmethod
    def region(region):
        """Transform the region component of an IIIF url and parse it into
        iiif2 keyword arguments

        see: http://iiif.io/api/image/2.0/#region
        e.g. /{identifier}/{region}/{size}/{rotation}/{quality}.{format}
        """
        if region == 'full':
            return {'full': region}
        percent = region.startswith('pct:')
        xywh = region.lstrip('pct:').split(',')
        dimensions = dict(zip(list('xywh'), xywh))
        dimensions['percent'] = percent
        return dimensions

    @staticmethod
    def rotation(rotation):
        return {
            'flip': rotation.startswith('!'),
            'degrees': rotation.lstrip('!')
            }

    @staticmethod
    def size(dimensions):
        if dimensions == 'full':
            return {'full': dimensions}

        if dimensions.startswith('pct:'):
            return {'percent': int(dimensions.lstrip('pct:')[1])}

        return dict(zip(list('wh'), dimensions.split(',')))
