VNT0_VERTEX_SIZE = 32
VNT1_VERTEX_SIZE = 20
VNT2_VERTEX_SIZE = 48
MATRIX_SIZE = 64
CHUNK_HEADER_SIZE = 8
SUBMODEL_SIZE = 256
IDX1_INDEX_SIZE = 1
IDX2_INDEX_SIZE = 2
IDX4_INDEX_SIZE = 4
FLOAT_SIZE = 4

# flags of the optional parameters of a light point in its submodel record, after its radius (as the simulator writes them)
LIGHT_SHADESELF = 0x1
LIGHT_NOSHADOWS = 0x2
LIGHT_SOFTFALLOFF = 0x4
LIGHT_LIGHTONLY = 0x8

TYPEID_TO_TYPENAME = {
    4: "Mesh",
    256: "Mesh",
    257: "FreeSpotLight",
    258: "Stars"
}

ANIMID_TO_ANIMTYPENAME = {
    -1: "true",
    0: "false",
    4: "seconds_jump",
    5: "minutes_jump",
    6: "hours_jump",
    7: "hours24_jump",
    8: "seconds",
    9: "minutes",
    10: "hours",
    11: "hours24",
    12: "billboard",
    13: "wind",
    14: "sky",
    256: "ik",
    257: "ik1",
    258: "ik2"
}