#!/usr/bin/env python
# -*-coding: utf-8 -*-

"""
    exc.py
    ~~~~~~
    Exceptions for IIIF Image 2.0 Library

    :copyright: (c) 2015 by Authors
    :license: see LICENSE for more details.
"""


class IIIF2Error(Exception):
    """Generic error class."""
    pass


class RegionArgumentError(IIIF2Error):
    """Raised when incorrect arguments supplies for Region"""
    pass


class SizeArgumentError(IIIF2Error):
    """Raised when incorrect arguments supplies for Size"""
    pass


class RotationArgumentError(IIIF2Error):
    """Raised when invalid degrees specified"""
    pass


class QualityArgumentError(IIIF2Error):
    """Raised when incorrect arguments supplies for Quality"""
    pass


class FormatArgumentError(IIIF2Error):
    """Raised when incorrect arguments supplies for Format"""
    pass
