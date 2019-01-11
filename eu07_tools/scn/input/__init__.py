from collections.abc import Iterator
import functools

from eu07_tools.utils.input import TokenStream
import eu07_tools.scn.structures as scnstruct

class SCNIterativeLoader(Iterator):
    def __init__(self, file):
        self._token_stream = TokenStream.from_file(file)
        self._iterator = self._load()

        self._element_loaders = {
            "atmo": self._load_atmo,
            "camera": self._load_camera,
            "config": self._load_config,
            "description": self._load_description,
            "event": self._load_event,
            "firstinit": self._load_firstinit,
            "include": self._load_include,
            "light": self._load_light,
            "lua": self._load_lua,
            "node": self._load_node,
            "origin": self._load_origin,
            "endorigin": self._load_endorigin,
            "rotate": self._load_rotate,
            "sky": self._load_sky,
            "test": self._load_test,
            "time": self._load_time,
            "trainset": self._load_trainset
        }

        self._event_loaders = {

        }

        self._node_loaders = {
            "triangles": self._load_node_triangles,
            "triangle_strip": self._load_node_triangle_strip,
            "triangle_fan": self._load_node_triangle_fan
        }

        self._get_token = self._token_stream.get_token
        self._get_tokens = self._token_stream.get_tokens
        self._get_tokens_before = self._token_stream.get_tokens_before

    @classmethod
    def from_file(cls, file):
        return cls(file)

    def __next__(self):
        return next(self._iterator)

    def _load(self):
        while True:
            token = self._token_stream.get_token().lower()

            if token == "":
                return

            load_element = self._element_loaders.get(token)

            if load_element:
                element = load_element()
                if element:
                    yield token, element

    def _load_atmo(self):
        atmo = scnstruct.SCNAtmo()
        atmo.sky_color = list(self._get_typed_tokens(3, float))
        atmo.fog_start = float(self._get_token())
        atmo.fog_end = float(self._get_token())
        
        if atmo.fog_end > 0:
            atmo.fog_color = list(self._get_typed_tokens(3, float))

        token = self._get_token().lower()

        if token != "endatmo":
            atmo.overcast = float(token)
            self._get_token()

        return atmo


    def _load_camera(self):
        camera = scnstruct.SCNCamera()
        camera.position = list(self._get_typed_tokens(3, float))
        camera.rotation = list(self._get_typed_tokens(3, float))

        token = self._get_token()

        if token != "endcamera":
            camera.index = int(token)
        else:
            pass # TODO: Automatic camera indexing

        return camera

    def _load_config(self):
        # TODO: Config loading
        self._get_tokens_before("endconfig")
        return None

    def _load_description(self):
        self._get_tokens_before("enddescription")
        return None

    def _load_event(self):
        self._get_tokens_before("endevent")
        return None

    def _load_firstinit(self):
        return True

    def _load_include(self):
        include = scnstruct.SCNInclude()
        include.path, *parameters = self._get_tokens_before("end")
        for p_value in parameters:
            include.append_parameter_value(p_value)

        return include

    def _load_light(self):
        self._get_tokens_before("endlight")
        return None

    def _load_lua(self):
        lua = scnstruct.SCNLua()
        lua.path = self._get_token()
        return lua

    def _load_node(self):
        max_distance = float(self._get_token())
        min_distance = float(self._get_token())
        name, subtype = self._get_tokens(2)

        load_node = self._node_loaders.get(subtype)

        if load_node:
            node = load_node(name)

        node.max_distance = max_distance
        node.min_distance = min_distance

        return node

    def _load_node_dynamic(self, name):
        dynamic = scnstruct.SCNNodeDynamic(name)
        dynamic.base_path, dynamic.map, dynamic.mmd_path = self._get_tokens(3)

        if not self._is_trainset_opened:
            dynamic.track_name = self._get_token()
            dynamic.offset = float(self._get_token())

        dynamic.driver_type = self._get_token()

        if self._is_trainset_opened:
            dynamic.coupling = self._get_token()
        else:
            dynamic.initial_velocity = float(self._get_token())
        
        dynamic.load_count = float(self._get_token())

        if dynamic.load_count > 0:
            dynamic.load_type = self._get_token()

        token = self._get_token()

        if token != "enddynamic":
            __, dynamic.destination, __ = self._get_tokens(3)

        return dynamic

    def _load_node_eventlauncher(self, name):
        launcher = scnstruct.SCNNodeEventlauncher(name)
        *launcher.location, launcher.radius = self._get_typed_tokens(4, float)
        launcher.key = self._get_token()
        launcher.delta_time = float(self._get_token())
        launcher.first_event_name, launcher.second_event_name = self._get_tokens(2)

        if launcher.second_event_name != "condition":
            launcher.memcell_name = self._get_tokens(2)
            launcher.check_mask = int(self._get_token)
        
        self._get_token() # endtag

        return launcher

    def _load_node_lines(self, name):
        return self._generic_load_lines(
            scnstruct.SCNNodeLines(name)
        )

    def _load_node_line_loop(self, name):
        return self._generic_load_lines(
            scnstruct.SCNNodeLineLoop(name)
        )

    def _load_node_line_strip(self, name):
        return self._generic_load_lines(
            scnstruct.SCNNodeLineStrip(name)
        )

    def _generic_load_lines(self, node):
        *node.color, node.thickness = self._get_typed_tokens(4, float)

        while True:
            token = self._get_token()

            if token == "endlines":
                break
            else:
                vertex_co = [float(token)] + list(self._get_typed_tokens(2, float))
                node.add_vertex(vertex_co)

        return node

    def _load_node_memcell(self, name):
        memcell = scnstruct.SCNNodeMemcell(name)
        memcell.location = self._get_typed_tokens(3, float)
        memcell.values[0] = self._get_token()
        memcell.values[1:] = self._get_typed_tokens(3, float)
        memcell.track_name = self._get_token()

        return memcell

    def _load_node_model(self, name):
        model = scnstruct.SCNNodeModel(name)
        *model.location, model.rotation_y = self._get_typed_tokens(4, float)
        model.path, model.map = self._get_tokens(2)

        token = self._get_token()

        if token == "lights":
            model.light_states = [float(ls) for ls in self._get_tokens_before("endmodel")]

        return model

    def _load_node_sound(self, name):
        sound = scnstruct.SCNNodeSound(name)
        sound.location = self._get_typed_tokens(3, float)
        sound.path = self._get_token()
        self._get_token()

        return sound


    def _load_node_track(self, name):
        # TODO: Track loading
        self._get_tokens_before("endtrack")
        return None

    def _load_node_traction(self, name):
        traction = scnstruct.SCNNodeTraction(name)

        traction.powersource_name = self._get_token()
        traction.nominal_voltage = float(self._get_token())
        traction.max_current = float(self._get_token())
        traction.resistivity = float(self._get_token())
        traction.wire_material_type = self._get_token()
        traction.wire_thickness = float(self._get_token())
        traction.damage_flag = int(self._get_token())
        p1 = list(self._get_typed_tokens(3, float))
        p2 = list(self._get_typed_tokens(3, float))
        p3 = list(self._get_typed_tokens(3, float))
        p4 = list(self._get_typed_tokens(3, float))
        traction.min_height, traction.segment_length = self._get_typed_tokens(2, float)
        traction.wires_type = int(self._get_token())
        
        if traction.wires_type != 0:
            traction.wire_offset = float(self._get_token())
        traction.visible = (True if self._get_token() == "vis" else False)
        
        token = self._get_token()

        if token == "parallel":
            traction.parallel_name = self._get_token()



    def _load_node_triangles(self, name):
        return self._generic_load_triangles(
            scnstruct.SCNNodeTriangles(name)
        )

    def _load_node_triangle_strip(self, name):
        return self._generic_load_triangles(
            scnstruct.SCNNodeTriangleStrip(name)
        )

    def _load_node_triangle_fan(self, name):
        return self._generic_load_triangles(
            scnstruct.SCNNodeTriangleFan(name)
        )


    def _generic_load_triangles(self, node):
        token = self._get_token()
        map_ = token

        if token == "material":
            self._get_token()
            ambient = list(self._get_typed_tokens(3, float))
            self._get_token()
            diffuse = list(self._get_typed_tokens(3, float))
            self._get_token()
            specular = list(self._get_typed_tokens(3, float))
            self._get_token()

            node.material = scnstruct.SCNTrianglesMaterial(ambient, diffuse, specular)
            map_ = self._get_token()
            
        node.map = map_

        # TODO: Optimize
        tokens = self._get_tokens_before("endtri")
        tokens = [token for token in tokens if token != "end"]
        num_verts = len(tokens) // 8

        for vi in range(num_verts):
            node.add_vertex(
                [float(x) for x in tokens[8 * vi : 8 * vi + 8]]
            )

        return node

    def _load_origin(self):
        vector = list(self._get_typed_tokens(3, float))
        return scnstruct.SCNOrigin(vector)

    def _load_endorigin(self):
        return True

    def _load_rotate(self):
        vector = list(self._get_typed_tokens(3, float))
        return scnstruct.SCNRotate(vector)

    def _load_sky(self):
        sky = scnstruct.SCNSky()
        sky.model_path, __ = self._get_tokens(2)
        return sky

    def _load_test(self):
        self._get_tokens_before("endtest")
        return None

    def _load_time(self):
        time = scnstruct.SCNTime()
        time.inital_time, time.sunset_time, time.sunrise_time = self._get_tokens(3)
        return time

    def _load_trainset(self):
        self._is_trainset_opened = True

        trainset = scnstruct.SCNTrainset()

        trainset.timetable_path, trainset.track_name = self._get_tokens(2)
        trainset.offset, trainset.velocity = self._get_typed_tokens(2, float)
        return trainset

    def _load_endtrainset(self):
        self._is_trainset_opened = False
        return True

    def _get_typed_tokens(self, count, type_):
        return (type_(self._get_token()) for _ in range(count))
