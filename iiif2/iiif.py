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

from PIL import Image, ImageFilter
from shutil import copyfileobj
from io import BytesIO
from . import exc


VALID_COLOR_MODES = {
    'color': 'RGB',
    'gray': 'L',
    'bitonal': '1',
    'default': None
    }

VALID_FILE_FMTS = {
    'jpg': {'im': 'JPEG', 'mime': 'image/jpeg'},
    'tif': {'im': 'TIFF', 'mime': 'image/tiff'},
    'png': {'im': 'PNG', 'mime': 'image/png'},
    'gif': {'im': 'GIF', 'mime': 'image/gif'},
    'jp2': {'im': 'JPEG 2000', 'mime': 'image/jp2'},
    'pdf': {'im': 'PDF', 'mime': 'application/pdf'},
    'swebp': {'im': 'WEBP', 'mime': 'image/webp'}
    }


class IIIF(object):

    @classmethod
    def render(cls, path, identifier, region, size, rotation, quality, fmt):
        """Executes complete IIIF Image 2.0 processing pipeline. Takes
        a **kwargs dict or keyword for each component. Returns an
        in-memory Tile file obj (StirngIO) in the desired fmt.

        params:1
            path - the resolved path of image file on disk
            identifier - iiif resource identifier
            region - a dictionary of kwargs to be passed to cls.crop
            size - a dictionary of kwargs to be passed to cls.scale

        usage:
            >>> IIIF.render(
            ...    identifier="abcd1234", region={"full": True},
            ...    size={"full": True}, rotation={"flip": False, "degrees": 0},
            ...    quality="default", fmt="jpg")
        """
        with Image.open(path) as im:
            return cls.format(
                cls.colorize(
                    cls.rotate(
                        cls.scale(
                            cls.crop(im, **region),
                            **size),
                        **rotation),
                    **quality),
                **fmt)

    @staticmethod
    def maximize(left, top, right, bottom, width, height):
        """Maximizes the dimensions of the four coordinates of a box
        (relative to its center) within a max width and height, or
        returns False if box values are impossible.
        """
        if right < left or bottom < top:
            raise exc.RegionArgumentError("Invalid region coordinates")

        left = 0 if left < 0 else width if left > width else left
        right = 0 if right < 0 else width if right > width else right
        top = 0 if top < 0 else height if top > height else top
        bottom = 0 if bottom < 0 else height if bottom > height else bottom
        return (left, top, right, bottom)

    @classmethod
    def crop(cls, im, full=False, x=None, y=None, w=None, h=None,
             percent=False):
        if full:
            return im
        if not any([x, y, w, h]):
            raise exc.RegionArgumentError(
                "x, y, w, h, or full must be specified"
                )
        iw, ih = im.size
        box = (int(round(x/100 * iw)),
               int(round(y/100 * ih)),
               int(round(x/100 * ih)) + int(round(w/100 * iw)),
               int(round(y/100 * ih)) + int(round(h/100 * ih))
               ) if percent else (int(x),
                                  int(y),
                                  int(x) + int(w),
                                  int(y) + int(h))

        return im.crop(cls.maximize(*box, width=iw, height=ih))

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
        if full:
            return im
        if not any([w, h, percent]):
            raise exc.SizeArgumentError(
                "full, w and or h, or percent must be specified"
                )

        iw, ih = im.size
        if w and h:
            width, height = w, h

        elif w and not h:
            # scale height to width, preserving aspect ratio
            width, height = w, int(round(ih * float(w / float(iw))))

        elif h and not w:
            # scale to height, preserving aspect ratio
            width, height = int(round(float(iw) * float(h / float(ih)))), h

        elif percent:
            width = int(round(iw * percent / 100)),
            height = int(round(ih * percent / 100))

        return im.resize((width, height), Image.BICUBIC)

    @classmethod
    def rotate(cls, im, degrees, flip=False):
        """First performs a vertical flip of the image (if specified)
        and then rotates the image the specified number of degrees.
        """
        if type(degrees) is not int:
            raise exc.RotationArgumentError("Degrees must be %s, not %s"
                                            % (type(int), type(degrees)))
        if degrees < 0 or degrees > 360:
            raise exc.RotationArgumentError("Invalid degrees: %s" % degrees)
        if flip:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if degrees:
            im = im.rotate(degrees, resample=Image.BICUBIC, expand=1)
        return im

    @classmethod
    def colorize(cls, im, mode="default"):
        """Colorizes the image using the appropriate mode"""
        if mode not in VALID_COLOR_MODES:
            raise exc.QualityArgumentError("Invalid color scale quality")

        # If color has a defined conversion type
        if VALID_COLOR_MODES[mode]:
            im = im.convert(VALID_COLOR_MODES[mode])

        # Unsharp Mask to increase local contrast in the image
        im = im.filter(
            ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=3)
            )
        return im

    @classmethod
    def format(cls, im, fmt="jpg"):
        """Returns an in-memory Tile file obj in a specific format"""
        ext = fmt.lower()
        if ext not in VALID_FILE_FMTS:
            raise exc.FormatArgumentError(
                "Invalid Tile file format. Valid options are: %s" %
                VALID_FILE_FMTS.keys())
        tile = Tile(ext=ext, mime=VALID_FILE_FMTS[ext]['mime'])
        im.save(tile, VALID_FILE_FMTS[ext]['im'])
        return tile


class Tile(BytesIO):

    def __init__(self, ext=None, mime='image/jpeg'):
        self.ext = ext
        self.mime = mime
        BytesIO.__init__(self)

    def save(self, path, ext=False):
        """Can be used by caching to save this in-memory Tile file
        (BytesIO buffer) to disk
        """
        filename = '%s.%s' % (path, self.ext) if ext else path
        with open(filename, 'w') as f:
            copyfileobj(self, f)

    def contents(self):
        return self.getvalue()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(exc_type, exc_value, traceback)
            self.close()
            return False
        return self

    def __enter__(self):
        self.seek(0)
        return self
