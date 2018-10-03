from eu07_tools.io import T3DLoader

import os
TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'loader_testfile.t3d')

def test_load_file():
    entries = T3DLoader().load_from_file(open(TESTDATA_FILENAME))

    report = [type_id for type_id, _ in entries]

    expected = [
        "submodel::mesh", 
        "include", 
        "submodel::freespotlight", 
        "submodel::stars"
    ]

    assert report == expected 