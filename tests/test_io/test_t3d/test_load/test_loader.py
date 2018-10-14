from eu07_tools.io import T3DLoader

import os
TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'loader_testfile.t3d')

def test_load_file():
    entries = T3DLoader().load_from_file(open(TESTDATA_FILENAME))

    report = [entry for entry in entries]

    expected_mesh = {
        "Parent": "none",
        "Type": "Mesh",
        "Name": "sub0",
        "Anim": "false",
        "Ambient": [180, 180, 180],
        "Diffuse": [180, 180, 180],
        "Specular": [229.5, 229.5, 229.5],
        "SelfIllum": 0.0,
        "Wire": False,
        "WireSize": 1.0,
        "Opacity": 100.0,
        "Map": "(podloga",
        "MaxDistance": 1000.0,
        "MinDistance": 0.0,
        "Transform": [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, -5.08919, 1.98218, 1.0
        ],
        "NumVerts": 6,
        "GEOMETRY": [
            [
                1, 
                -1.5, 0.8, 0.0, 0.0, 1.0,
                -1.5, -0.8, 0.0, 0.0, 0.0,
                1.5, 0.8, 0.0, 1.0, 1.0,
            ],
            [
                -1,
                1.5, -0.8, 0.0, 1.0, 2.0, 3.0, 1.0, 0.0,
                1.5, 0.8, 0.0, 1.0, 2.0, 3.0, 1.0, 1.0,
                -1.5, -0.8, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0,
            ]
        ]
    }

    expected_include = ["example.t3d", "param", "pam", "pam"]

    expected_freespot = {
        "Parent": "sub0",
        "Type": "FreeSpotLight",
        "Name": "sub1",
        "Anim": "false",
        "Diffuse": [255.0, 255.0, 255.0],
        "SelfIllum": 1.0,
        "NearAttenStart": 40.0,
        "NearAttenEnd": 0.0,
        "UseNearAtten": False,
        "FarAttenDecayType": 1.0,
        "FarDecayRadius": 25.0,
        "FalloffAngle": 119.49999,
        "HotspotAngle": 119.49999,
        "MaxDistance": -1.0,
        "MinDistance": 0.0,
        "Transform": [
            0.4750, 0.0, 0.87966, 0.0,
            0.0, 1.0, 0.0, 0.0
            -0.87966, 0.0, 0.4756, 0.0,
            4.18291, -0.03021, 6.29331, 1.0
        ]
    }

    expected_stars = {
        "Parent": "sub0",
        "Type": "Stars",
        "Name": "sub2",
        "Anim": "false",
        "Diffuse": [180.0, 180.0, 180.0],
        "SelfIllum": 0.0,
        "MaxDistance": 1000.0,
        "MinDistance": 0.0,
        "Transform": [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, -5.08919, 1.98218, 1.0,
        ],
        "NumVerts": 3,
        "GEOMETRY": [
            [
                1,
                -1.54021, 0.87027, 0.0, 0.0, 1.0, 
                -1.54021, -0.87027, 0.0, 0.0, 0.0, 
                1.54403, 0.87027, 0.0, 1.0, 1.0, 
            ]
        ]
    }

    expected = [
        ("submodel", expected_mesh), 
        ("include", expected_include), 
        ("submodel", expected_freespot), 
        ("submodel", expected_stars)
    ]

    assert report == expected 