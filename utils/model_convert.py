def e3d_to_t3d(e3d_model):
    from ..t3d import create_submodel

    for e3d_sm in e3d_model.submodels:
        
        t3d_sm = create_submodel(e3d_sm.type, e3d_sm.name)

        t3d_sm.diffuse_color = [x * 255 for x in e3d_sm.diffuse_color[:3]]
        t3d_sm.anim = e3d_sm.anim
        t3d_sm.max_distance = e3d_sm.max_distance
        t3d_sm.min_distance = e3d_sm.min_distance
        t3d_sm.selfillum = e3d_sm.selfillum

        t3d_sm.transform = e3d_sm.transform
        mat = t3d_sm.transform
        # RHS to LHS coordinate conversion
        mat[1], mat[2] = mat[2], mat[1]
        mat[13], mat[14] = mat[14], mat[13]
        mat[4], mat[8] = mat[8], mat[4]
        mat[5], mat[10] = mat[10], mat[5]
        mat[6], mat[9] = mat[9], mat[6]

        t3d_sm.parent_name = e3d_sm.parent.name if e3d_sm.parent else "none"
        
        if e3d_sm.type == "Mesh":
            t3d_sm.ambient_color = [x * 255 for x in e3d_sm.ambient_color[:3]]
            t3d_sm.specular_color = [x * 255 for x in e3d_sm.specular_color[:3]]
            t3d_sm.wire_size = e3d_sm.wire_size
            t3d_sm.map = e3d_sm.map
            
            t3d_sm.geometry = e3d_sm.get_geometry().to_triangles()

        elif e3d_sm.type == "FreeSpotLight":
            t3d_sm.near_atten_start = e3d_sm.near_atten_start
            t3d_sm.near_atten_end = e3d_sm.near_atten_end
            t3d_sm.use_near_atten = e3d_sm.use_near_atten
            t3d_sm.far_atten_decay_type = e3d_sm.far_atten_decay_type
            t3d_sm.far_decay_radius = e3d_sm.far_decay_radius
            if e3d_sm.hotspot_power != 1.0:
                t3d_sm.hotspot_power = e3d_sm.hotspot_power * 100
            if e3d_sm.radius > 0.0:
                t3d_sm.radius = e3d_sm.radius
            if e3d_sm.shade_self:
                t3d_sm.shade_self = True
            if not e3d_sm.cast_shadows:
                t3d_sm.cast_shadows = False
            if e3d_sm.soft_falloff:
                t3d_sm.soft_falloff = True
            if e3d_sm.light_only:
                t3d_sm.light_only = True
            # TODO: cos_falloff_angle, cos_hotspot_angle - how to translate to t3d?        

        elif e3d_sm.type == "Stars":
            for vertex in e3d_sm.vertices:
                t3d_sm.stars.new(vertex.location, vertex.mapping.u)

        yield t3d_sm

def t3d_to_e3d(t3d_model):
    pass


        
