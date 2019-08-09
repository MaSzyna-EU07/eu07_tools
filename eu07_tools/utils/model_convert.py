import eu07_tools

def e3d_to_t3d(e3d_model):
    for e3d_sm in e3d_model.submodels:
        
        t3d_sm = eu07_tools.t3d.create_submodel(e3d_sm.type, e3d_sm.name)

        t3d_sm.diffuse_color = [x * 255 for x in e3d_sm.diffuse_color[:3]]
        t3d_sm.anim = e3d_sm.anim
        t3d_sm.max_distance = e3d_sm.max_distance
        t3d_sm.min_distance = e3d_sm.min_distance
        t3d_sm.selfillum = e3d_sm.selfillum
        t3d_sm.transform = e3d_sm.transform
        t3d_sm.parent_name = e3d_sm.parent.name if e3d_sm.parent else "none"
        
        if e3d_sm.type == "Mesh":
            t3d_sm.ambient_color = [x * 255 for x in e3d_sm.ambient_color[:3]]
            t3d_sm.specular_color = [x * 255 for x in e3d_sm.specular_color[:3]]
            t3d_sm.wire_size = e3d_sm.wire_size
            t3d_sm.map = e3d_sm.map
            
            num_triangles = e3d_sm.num_verts // 3
            for x in range(num_triangles):
                vertices = e3d_sm.vertices[x*3:x*3+3]

                for vertex in vertices:
                    vertex.location = eu07_tools.utils.switch_coordinate_system(vertex.location)

                t3d_sm.triangles.new(vertices, -1)

        elif e3d_sm.type == "FreeSpotLight":
            t3d_sm.near_atten_start = e3d_sm.near_atten_start
            t3d_sm.near_atten_end = e3d_sm.near_atten_end
            t3d_sm.use_near_atten = e3d_sm.use_near_atten
            t3d_sm.far_atten_decay_type = e3d_sm.far_atten_decay_type
            t3d_sm.far_decay_radius = e3d_sm.far_decay_radius
            # TODO: cos_falloff_angle, cos_hotspot_angle - how to translate to t3d?        

        elif e3d_sm.type == "Stars":
            for vertex in e3d_sm.vertices:
                t3d_sm.stars.new(vertex.location, vertex.mapping.u)

        
        yield t3d_sm

def t3d_to_e3d(self):
    pass


        
