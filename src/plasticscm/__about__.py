# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

__all__ = ('__title__', '__summary__', '__uri__', '__version_info__',
           '__version__', '__author__', '__maintainer__', '__email__',
           '__copyright__', '__license__')

__title__        = "plasticscm"
__summary__      = "Python package providing access to the PlasticSCM client API."
__uri__          = "https://pypi.org/project/plasticscm/"
__version_info__ = type("version_info", (), dict(serial=5,
                        major=0, minor=1, micro=0, releaselevel="alpha"))
__version__      = "{0.major}.{0.minor}.{0.micro}{1}{2}".format(__version_info__,
                   dict(final="", alpha="a", beta="b", rc="rc")[__version_info__.releaselevel],
                   "" if __version_info__.releaselevel == "final" else __version_info__.serial)
__author__       = "Adam Karpierz"
__maintainer__   = "Adam Karpierz"
__email__        = "adam@karpierz.net"
__copyright__    = "Copyright (c) 2019-2020, {0}".format(__author__)
__license__      = "zlib/libpng License ; {0}".format(
                   "https://opensource.org/licenses/zlib")
