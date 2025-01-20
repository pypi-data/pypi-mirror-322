"""
"""
import sys

try:
    __PYGDK_SETUP__
except NameError:
    __PYGDK_SETUP__ = False

if __PYGDK_SETUP__:
    sys.stderr.write('Running from pygdk source directory.\n')
else:
    from . import core
    from .core import (
        Gk, GkLabel
    )

    # from . import GkMix
    # from .GkMix import (

    # )

    __all__ = list(
        set(core.__all__) 
    )