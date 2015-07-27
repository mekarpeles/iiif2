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

from . import exc


class IIIF(object):

    VALID_COLORS = ['color', 'gray', 'bitonal', 'default']
    VALID_EXTS = ['jpg', 'tif', 'png', 'gif', 'jp2', 'pdf']

    @classmethod
    def slice(cls, im, full=False, x=None, y=None, w=None, h=None,
              percent=False):
        if not any(x, y, w, h, full):
            raise exc.RegionArgumentError(
                "x, y, w, h, or full must be specified"
                )

    @staticmethod
    def scale(im, full=False, w=None, h=None, percent=None):
        """See http://iiif.io/api/image/2.0/#size

        params:
               full - The extracted region is not scaled, and is
                      returned at its full size.
                  w - width to scale slice (if width, height optional)
                  h - height to scale slice (if height, width
                      optional)
            percent - The width and height of the returned image is
                      scaled to n% of the width and height of the
                      extracted region. The aspect ratio of the
                      returned image is the same as that of the
                      extracted region.
        """
        if not any(full, w, h, percent):
            raise exc.SizeArgumentError(
                "full, w and or h, or percent must be specified"
                )

    @classmethod
    def rotate(cls, im, degrees, flip=False):
        if type(degrees) is not int or degrees < 0 or degrees > 360:
            raise exc.RotationArgumentError("Invalid dimensions")

    @classmethod
    def colorize(cls, im, color="default"):
        if color not in cls.VALID_COLORS:
            raise exc.QualityArgumentError("Invalid color scale quality")

    @classmethod
    def format(cls, im, ext="jpg"):
        if ext not in cls.VALID_EXTS:
            raise exc.FormatArgumentError("Invalid file format.")
