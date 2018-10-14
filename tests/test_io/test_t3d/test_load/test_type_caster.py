import pytest

from eu07_tools.io.t3d.load.type_caster import T3DTypeCaster

type_caster = T3DTypeCaster()

def test_cast_rgb():
    casted_value = type_caster.cast_property_value(
        "Diffuse", ["255", "34.5", "0"]
    )
    assert casted_value == [255.0, 34.5, 0]


def test_cast_transform():
    casted_values = type_caster.cast_property_value(
        "Transform", ["1", "2", "3", "4", "5", "6", "7", "8"]
    )
    assert casted_values == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

    
def test_cast_bool():
    casted_value = type_caster.cast_property_value(
        "Wire", "true"
    )
    assert casted_value is True

    casted_value = type_caster.cast_property_value(
        "UseNearAtten", "false"
    )
    assert casted_value is False


def test_cast_self_illum():
    casted_value = type_caster.cast_property_value(
        "SelfIllum", "true"
    )
    assert casted_value == 1.0

    casted_value = type_caster.cast_property_value(
        "SelfIllum", "false"
    )
    assert casted_value == 0.0

    casted_value = type_caster.cast_property_value(
        "SelfIllum", "1.25"
    )
    assert casted_value == 1.25

def test_cast_geometry():
    casted_value = type_caster.cast_property_value(
        "GEOMETRY", [
            [
                "1",
                "1", "2", "3", "4", "5",
                "1", "2", "3", "4", "5",
                "1", "2", "3", "4", "5",
            ],
            [
                "-1",
                "1", "2", "3", "4", "5"
            ]
        ]
    )

    expected_value = [
        [
            1.0,
            1.0, 2.0, 3.0, 4.0, 5.0,
            1.0, 2.0, 3.0, 4.0, 5.0,
            1.0, 2.0, 3.0, 4.0, 5.0
        ],
        [
            -1.0,
            1.0, 2.0, 3.0, 4.0, 5.0,
        ]
    ]

    assert casted_value == expected_value