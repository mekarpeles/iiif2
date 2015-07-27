

class IIIF2Error(Exception):
    """Generic error class."""
    pass


class RegionArgumentError(IIIF2Error):
    """Raised when incorrect arguments supplies for Region"""
    pass


class SizeArgumentError(IIIF2Error):
    """Raised when incorrect arguments supplies for Size"""
    pass


class QualityArgumentError(IIIF2Error):
    """Raised when incorrect arguments supplies for Quality"""
    pass


class FormatArgumentError(IIIF2Error):
    """Raised when incorrect arguments supplies for Format"""
    pass
