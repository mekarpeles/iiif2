#!/usr/bin/env python
# -*-coding: utf-8 -*-

"""
    iiif.py
    ~~~~~~~
    An API for processing images according to the IIIF Image Server
    2.0 standard. http://iiif.io/api/image/2.0/

    :copyright: (c) 2015 by Authors
    :license: see LICENSE for more details.
"""


class IIIF(object):

    COLOR_SCALES = ['color', 'gray', 'bitonal', 'default']

    @classmethod
    def slice(cls, im, x=None, y=None, w=None, h=None,
              full=False, percent=False):
        if not any(x, y, w, h, full):
            raise Exception("x, y, w, h, or full must be specified")
        pass

    @classmethod
    def scale(cls, im, full=False, w=None, h=None, percent=None):
        if not any(full, w, h, percent):
            raise Exception("full, w and or h, or percent must be specified")
        pass

    @classmethod
    def rotate(cls, im, degrees, flip=False):
        pass

    @classmethod
    def colorize(cls, im, color="default"):
        if scale not in COLOR_SCALES:
            raise Exception("Invalid color scale quality")

    @classmethod
    def format(cls, im, ext="jpg"):
        if scale not in COLOR_SCALES:
            raise Exception("Invalid color scale quality")
