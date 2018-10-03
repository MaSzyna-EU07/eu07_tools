from eu07_tools.structs.t3d import T3DMeshSubmodel, T3DFreeSpotLightSubmodel, T3DStarsSubmodel

def build_submodel(d):
    type_ = d["type"].lower()
    if type_ == "mesh":
        submodel = T3DMeshSubmodel(d["name"])
        submodel.ambient = d["ambient"]
        submodel.specular = d["specular"]
        submodel.wire = d["wire"]
        submodel.wire_size = d["wiresize"]
        submodel.opacity = d["opacity"]
        submodel.map = d["map"]

        for geometry_unit in d["geometry"]:
            smooth = geometry_unit[0]
            vertices = geometry_unit[1:]
            submodel.add_triangle(vertices, smooth)

    elif type_ == "freespotlight":
        submodel = T3DFreeSpotLightSubmodel(d["name"])
        submodel.near_atten_start = d["nearattenstart"]
        submodel.near_atten_end = d["nearattenend"]
        submodel.use_near_atten = d["usenearatten"]
        submodel.far_atten_decay_type = d["farattendecaytype"]
        submodel.far_decay_radius = d["fardecayradius"]
        submodel.hotspot_angle = d["hotspotangle"]
        submodel.falloff_angle = d["falloffangle"]

    elif type_ == "stars":
        submodel = T3DStarsSubmodel(d["name"])

        for geometry_unit in d["geometry"]:
            stars = geometry_unit[1:]
            for star in stars:
                position = star[:3]
                encoded_color = int(star[3])
                color = (
                    ((encoded_color) & 0xff),
                    ((encoded_color >> 8) & 0xff),
                    ((encoded_color >> 16) & 0xff)
                )

                submodel.add_star(position, color)

    submodel.parent_name = d["parent"]
    submodel.anim = d["anim"]
    submodel.diffuse = d["diffuse"]
    submodel.self_illum = d["selfillum"]
    submodel.max_distance = d["maxdistance"]
    submodel.min_distance = d["mindistance"]
    submodel.transform = d["transform"]

    type_id = f"submodel::{type_}"
    return type_id, submodel
