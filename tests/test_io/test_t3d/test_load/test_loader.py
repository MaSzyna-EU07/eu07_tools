from eu07_tools.io import T3DLoader

import os
TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'loader_testfile.t3d')

def test_load_file():
    entries = T3DLoader().load_from_file(open(TESTDATA_FILENAME))

    expected = [
        "<T3DMeshSubmodel: sub0>",
        "<IncludedFile(path=example.t3d, params=('param', 'pam', 'pam'))>",
        "<T3DFreeSpotLightSubmodel: sub1>",
        "<T3DStarsSubmodel: sub2>",
    ]

    report = [repr(entry) for entry in entries]

    assert report == expected 