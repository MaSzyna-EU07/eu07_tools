import warnings

try:
    from .input import load
except ImportError:
    warnings.warn("You are using non-dev eu07_tools version. e3d.load function is not present.")
from .output import dump
from .structures import create_model