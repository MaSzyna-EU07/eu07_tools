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