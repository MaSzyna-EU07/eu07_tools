import eu07_tools.t3d

class ModelConverter:
    def __init__(self):
        self._TYPEID_TO_TYPENAME = {
            4: "Mesh",
            256: "Mesh",
            257: "FreeSpotLight",
            258: "Stars"
        }

        self._ANIMID_TO_ANIMTYPENAME = {
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

        self._parenting = {}  

    def e3d_to_t3d(self, e3d):
        t3d_submodels = []

        for submodel_id, e3d_sm in enumerate(e3d.submodels):

            type_ = self._TYPEID_TO_TYPENAME[e3d_sm.submodel_type_id]
            name = e3d.names[e3d_sm.name_id]
            t3d_sm = eu07_tools.t3d.create_submodel(type_, name)

            self._put_parenting(submodel_id, e3d_sm)

            t3d_sm.diffuse_color = e3d_sm.diffuse_color[:3] * 255
            t3d_sm.anim = self._ANIMID_TO_ANIMTYPENAME[e3d_sm.anim_id]
            t3d_sm.max_distance = e3d_sm.max_distance
            t3d_sm.min_distance = e3d_sm.min_distance
            t3d_sm.selfillum = e3d_sm.selfillum

            if e3d_sm.matrix_id != -1:
                t3d_sm.transform = e3d.matrices[e3d_sm.matrix_id]

            if type_ == "Mesh":
                t3d_sm.ambient_color = e3d_sm.ambient_color[:3] * 255
                t3d_sm.specular_color = e3d_sm.specular_color[:3] * 255
                t3d_sm.wire_size = e3d_sm.wire_size
                t3d_sm.map = e3d.materials[e3d_sm.material_id]
                
                vertices = e3d.vertices[
                    e3d_sm.first_vertex_id:
                    e3d_sm.first_vertex_id + e3d_sm.num_verts
                ]

                for x in range(len(vertices) // 3):
                    t3d_sm.triangles.new(
                        vertices[x*3:x*3+3], -1
                    )
                
            elif type_ == "FreeSpotLight":
                t3d_sm.near_atten_start = e3d_sm.near_atten_start
                t3d_sm.near_atten_end = e3d_sm.near_atten_end
                t3d_sm.use_near_atten = e3d_sm.use_near_atten
                t3d_sm.far_atten_decay_type = e3d_sm.far_atten_decay_type
                t3d_sm.far_decay_radius = e3d_sm.far_decay_radius
                # TODO: cos_falloff_angle, cos_hotspot_angle - how to translate to t3d?        

            elif type_ == "Stars":
                vertices = e3d_sm.vertices[
                    e3d_sm.first_vertex_id:
                    e3d_sm.first_vertex_id + e3d_sm.num_verts
                ]

                for vertex in vertices:
                    t3d_sm.stars.new(vertex.location, vertex.mapping.u)

            t3d_submodels.append(t3d_sm)
        
        self._set_parenting(t3d_submodels, e3d)

        return t3d_submodels

    def _put_parenting(self, submodel_id, e3d_sm):
        self._parenting[submodel_id] = []
        self._parenting[submodel_id].append(e3d_sm.first_child_id)

        for parent_id, child_ids in self._parenting.items():
            if submodel_id in child_ids:
                self._parenting[parent_id].append(e3d_sm.next_id)

    def _set_parenting(self, t3d_submodels, e3d):
        for sm_id, t3d_submodel in enumerate(t3d_submodels):
            for parent_id, child_ids in self._parenting.items():
                if sm_id in child_ids:
                    name_id = e3d.submodels[parent_id].name_id
                    parent_name = e3d.names[name_id]
                    t3d_submodel.parent_name = parent_name

        
