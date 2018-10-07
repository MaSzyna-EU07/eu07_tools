import pytest

from ..utils import make_fake_file
from eu07_tools.io.scn.loader import SCNLoader


# class Test_Loader:
#     def setup(self):
#         self.loader = SCNLoader()

#     def test_load_atmo(self):
#         file = make_fake_file(
#             "atmo 255 255 255 100 10 255 255 255 0.5 endatmo\n" # All parameters
#             "atmo 255 255 255 10 0 0.5 endatmo\n" # No fog color
#             "atmo 255 255 255 10 0 endatmo\n" # No fog color & overcast
#         )
