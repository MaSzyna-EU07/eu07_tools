import eu07_tools.t3d

_TYPEID_TO_TYPENAME = {
    4: "Mesh",
    256: "Mesh",
    257: "FreeSpotLight",
    258: "Stars"
}

_ANIMID_TO_ANIMTYPENAME = {

}

def e3d_to_t3d(e3d):
    for e3d_sm in e3d.submodels:

        type_ = _TYPEID_TO_TYPENAME[e3d_sm.type_id]
        name = e3d.names[e3d_sm.name_id]
        t3d_sm = eu07_tools.t3d.create_submodel(type_, name)

        # Set common properties
        # TODO: Parenting

        t3d_sm.diffuse_color = e3d_sm.diffuse_color
        t3d_sm.anim = _ANIMID_TO_ANIMTYPENAME[e3d_sm.anim_id]
        t3d_sm.max_distance = e3d_sm.max_distance
        t3d_sm.min_distance = e3d_sm.min_distance

        if type_ == "Mesh":
            t3d_sm.ambient_color = e3d_sm.ambient_color
            t3d_sm.specular_color = e3d_sm.specular_color
            t3d_sm.wire_size = e3d_sm.wire_size
            
            vertices = e3d_sm.vertices[
                e3d_sm.first_vertex_id:
                e3d_sm.first_vertex_id + e3d_sm.num_verts
            ]

            for vertex in vertices:
                t3d_sm.
            