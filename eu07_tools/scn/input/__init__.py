from collections.abc import Iterator
import functools

from eu07_tools.utils.input import TextScanner
import eu07_tools.scn.structures as scnstruct

def load(file):
    return SCNIterativeLoader(file)

class SCNIterativeLoader(Iterator):
    def __init__(self, file):
        self._scanner = TextScanner.from_file(file)
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
            "trainset": self._load_trainset,
            "endtrainset": self._load_endtrainset,
        }


        self._node_loaders = {
            "dynamic": self._load_node_dynamic,
            "model": self._load_node_model,
            "track": self._load_node_track,
            "triangles": self._load_node_triangles,
            "triangle_strip": self._load_node_triangle_strip,
            "triangle_fan": self._load_node_triangle_fan,
        }


    @classmethod
    def from_file(cls, file):
        return cls(file)

    def __next__(self):
        return next(self._iterator)

    def _load(self):
        while True:
            token = self._scanner.read_string().lower()

            if token == "":
                return

            load_element = self._element_loaders.get(token)

            if load_element:
                element = load_element()
                if element:
                    yield element

    def _load_atmo(self):
        atmo = scnstruct.SCNAtmo()
        atmo.sky_color = self._scanner.read_floats(3)
        atmo.fog_start = self._scanner.read_float()
        atmo.fog_end = self._scanner.read_float()
        
        if atmo.fog_end > 0:
            atmo.fog_color = self._scanner.read_floats(3)

        token = self._scanner.read_string().lower()

        if token != "endatmo":
            atmo.overcast = float(token)
            self._scanner.read_string()

        return atmo


    def _load_camera(self):
        camera = scnstruct.SCNCamera()
        camera.position = self._scanner.read_floats(3)
        camera.rotation = self._scanner.read_floats(3)

        token = self._scanner.read_string()

        if token != "endcamera":
            camera.index = int(token)
        else:
            pass # TODO: Automatic camera indexing

        return camera

    def _load_config(self):
        # TODO: Config loading
        self._scanner.get_strings_before("endconfig")
        return None

    def _load_description(self):
        self._scanner.get_strings_before("enddescription")
        return None

    def _load_event(self):
        

        self._scanner.get_strings_before("endevent")

        return None

    def _load_firstinit(self):
        return scnstruct.SCNFirstInit()

    def _load_include(self):
        include = scnstruct.SCNInclude()
        include.path, *parameters = self._scanner.get_strings_before("end")
        for p_value in parameters:
            include.append_parameter_value(p_value)

        return include

    def _load_light(self):
        self._scanner.get_strings_before("endlight")
        return None

    def _load_lua(self):
        lua = scnstruct.SCNLua()
        lua.path = self._scanner.read_string()
        return lua

    def _load_node(self):
        max_distance = self._scanner.read_float()
        min_distance = self._scanner.read_float()
        name, subtype = self._scanner.read_strings(2)

        load_node = self._node_loaders.get(subtype)

        if load_node:
            node = load_node(name)

            node.max_distance = max_distance
            node.min_distance = min_distance

            return node

    def _load_node_dynamic(self, name):
        dynamic = scnstruct.SCNNodeDynamic(name)
        dynamic.base_path, dynamic.map, dynamic.mmd_path = self._scanner.read_strings(3)

        if not self._is_trainset_opened:
            dynamic.track_name = self._scanner.read_string()

        dynamic.offset = self._scanner.read_float()
        dynamic.driver_type = self._scanner.read_string()

        if self._is_trainset_opened:
            dynamic.coupling = self._scanner.read_string()
        else:
            dynamic.initial_velocity = self._scanner.read_float()
        
        dynamic.load_count = self._scanner.read_float()

        if dynamic.load_count > 0:
            dynamic.load_type = self._scanner.read_string()

        token = self._scanner.read_string()

        if token != "enddynamic":
            __, dynamic.destination, __ = self._scanner.read_strings(3)

        return dynamic

    def _load_node_eventlauncher(self, name):
        launcher = scnstruct.SCNNodeEventlauncher(name)
        *launcher.location, launcher.radius = self._scanner.read_floats(4)
        launcher.key = self._scanner.read_string()
        launcher.delta_time = self._scanner.read_float()
        launcher.first_event_name, launcher.second_event_name = self._scanner.read_strings(2)

        if launcher.second_event_name != "condition":
            launcher.memcell_name = self._scanner.read_strings(2)
            launcher.check_mask = self._scanner.read_int()
        
        self._scanner.read_string() # endtag

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
        *node.color, node.thickness = self._scanner.read_floats(4)

        while True:
            token = self._scanner.read_string()

            if token == "endlines":
                break
            else:
                vertex_co = [float(token)] + self._scanner.read_floats(2)
                node.add_vertex(vertex_co)

        return node

    def _load_node_memcell(self, name):
        memcell = scnstruct.SCNNodeMemcell(name)
        memcell.location = self._scanner.read_floats(3)
        memcell.values[0] = self._scanner.read_string()
        memcell.values[1:] = self._scanner.read_floats(3)
        memcell.track_name = self._scanner.read_string()

        return memcell

    def _load_node_model(self, name):
        model = scnstruct.SCNNodeModel(name)
        *model.location, model.rotation_y = self._scanner.read_floats(4)
        model.path, model.map = self._scanner.read_strings(2)

        model.light_states = [int(s) for s in self._scanner.get_strings_before("endmodel")]

        return model

    def _load_node_sound(self, name):
        sound = scnstruct.SCNNodeSound(name)
        sound.location = self._scanner.read_floats(3)
        sound.path = self._scanner.read_string()
        self._scanner.read_string()

        return sound


    def _load_node_track(self, name):
        # TODO: Track loading
        subtype = self._scanner.read_string().lower()

        if subtype == "normal":
            track = scnstruct.SCNNodeTrackNormal(name)
        elif subtype == "road":
            track = scnstruct.SCNNodeTrackRoad(name)
        elif subtype == "river":
            track = scnstruct.SCNNodeTrackRiver(name)
        elif subtype == "switch":
            track = scnstruct.SCNNodeTrackSwitch(name)
        elif subtype == "cross":
            track = scnstruct.SCNNodeTrackCross(name)
        elif subtype == "tributary":
            track = scnstruct.SCNNodeTrackTributary(name)
        elif subtype == "turn":
            track = scnstruct.SCNNodeTrackTurn(name)
        elif subtype == "table":
            track = scnstruct.SCNNodeTrackTable(name)

        track.length = self._scanner.read_float()
        track.width = self._scanner.read_float()
        track.friction = self._scanner.read_float()
        track.sound_distance = self._scanner.read_float()
        track.quality_flag = self._scanner.read_int()
        track.damage_flag = self._scanner.read_int()
        track.environment = self._scanner.read_string()
        track.visible = (self._scanner.read_string() == "vis")
        track.material1 = self._scanner.read_string()
        track.mapping_length = self._scanner.read_float()
        track.material2 = self._scanner.read_string()
        track.tex_param1 = self._scanner.read_string()
        track.tex_param2 = self._scanner.read_string()
        track.tex_param3 = self._scanner.read_string()

        track.segments[0].p1 = self._scanner.read_floats(3)
        track.segments[0].p1.roll = self._scanner.read_float()
        track.segments[0].cv1 = self._scanner.read_floats(3)
        track.segments[0].cv2 = self._scanner.read_floats(3)
        track.segments[0].p2 = self._scanner.read_floats(3)
        track.segments[0].p2.roll = self._scanner.read_float()
        track.segments[0].radius = self._scanner.read_float()

        is_junction = (subtype in "switch cross tributary")
        if is_junction:
            track.segments[1].p1 = self._scanner.read_floats(3)
            track.segments[1].p1.roll = self._scanner.read_float()
            track.segments[1].cv1 = self._scanner.read_floats(3)
            track.segments[1].cv2 = self._scanner.read_floats(3)
            track.segments[1].p2 = self._scanner.read_floats(3)
            track.segments[1].p2.roll = self._scanner.read_float()
            track.segments[1].radius = self._scanner.read_float()

        
        while True:
            token = self._scanner.read_string()

            if token == "endtrack":
                break
            elif token == "event0":
                track.event0 = self._scanner.read_string()
            elif token == "event1":
                track.event1 = self._scanner.read_string()
            elif token == "event2":
                track.event2 = self._scanner.read_string()
            elif token == "eventall0":
                track.eventall0 = self._scanner.read_string()
            elif token == "eventall1":
                track.eventall1 = self._scanner.read_string()
            elif token == "eventall2":
                track.eventall2 = self._scanner.read_string()
            elif token == "isolated":
                track.isolated = self._scanner.read_string()
            elif token == "overhead":
                track.overhead = self._scanner.read_int()
            elif token == "angle1":
                track.angle1 = self._scanner.read_int()
            elif token == "angle2":
                track.angle2 = self._scanner.read_int()
            elif token == "fouling1":
                track.fouling1 = self._scanner.read_string()
            elif token == "fouling2":
                track.fouling2 = self._scanner.read_string()
            elif token == "vradius":
                track.vradius = self._scanner.read_float()
            elif token == "trackbed":
                track.trackbed = self._scanner.read_string()
            elif token == "railprofile":
                track.railprofile = self._scanner.read_string()

        return track

    def _load_node_traction(self, name):
        traction = scnstruct.SCNNodeTraction(name)

        traction.powersource_name = self._scanner.read_string()
        traction.nominal_voltage = self._scanner.read_float()
        traction.max_current = self._scanner.read_float()
        traction.resistivity = self._scanner.read_float()
        traction.wire_material_type = self._scanner.read_string()
        traction.wire_thickness = self._scanner.read_float()
        traction.damage_flag = self._scanner.read_int()
        traction.p1 = self._scanner.read_floats(3)
        traction.p2 = self._scanner.read_floats(3)
        traction.p3 = self._scanner.read_floats(3)
        traction.p4 = self._scanner.read_floats(3)
        traction.min_height = self._scanner.read_float()
        traction.segment_length = self._scanner.read_float()
        traction.wires_type = self._scanner.read_int()
        
        if traction.wires_type != 0:
            traction.wire_offset = self._scanner.read_float()
        traction.visible = (self._scanner.read_string() == "vis")
        
        token = self._scanner.read_string()

        if token == "parallel":
            traction.parallel_name = self._scanner.read_string()

        return traction

    def _load_node_tractionpowersource(self, name):
        power_source = scnstruct.SCNNodeTractionPowerSource(name)
        power_source.location = self._scanner.read_floats(3)
        power_source.nominal_voltage = self._scanner.read_float()
        power_source.voltage_frequency = self._scanner.read_float()
        power_source.internal_resistance = self._scanner.read_float()
        power_source.max_output_current = self._scanner.read_float()
        power_source.fast_fuse_timeout = self._scanner.read_float()
        power_source.fast_fuse_repetition = self._scanner.read_int()
        power_source.slow_fuse_timeout = self._scanner.read_float()

        optional = list(self._scanner.get_strings_before("end"))

        power_source.recuperation = ("recuperation" in optional)
        power_source.section = ("section" in optional)

        return power_source

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
        map_ = "none"
        token = self._scanner.read_string()

        if token == "material":
            self._scanner.read_string()
            ambient = self._scanner.read_floats(3)
            self._scanner.read_string()
            diffuse = self._scanner.read_floats(3)
            self._scanner.read_string()
            specular = self._scanner.read_floats(3)
            self._scanner.read_string()

            node.material = scnstruct.SCNTrianglesMaterial(ambient, diffuse, specular)
            map_ = self._scanner.read_string()
            
        node.map = map_

        vertex_endmark = ""
        while vertex_endmark != "endtri":
            node.vertices.new(self._scanner.read_floats(8))
            vertex_endmark = self._scanner.read_string()
        
        return node

    def _load_origin(self):
        vector = self._scanner.read_floats(3)
        return scnstruct.SCNOrigin(vector)

    def _load_endorigin(self):
        return scnstruct.SCNEndOrigin()

    def _load_rotate(self):
        vector = self._scanner.read_floats(3)
        return scnstruct.SCNRotate(vector)

    def _load_sky(self):
        sky = scnstruct.SCNSky()
        sky.model_path, __ = self._scanner.read_strings(2)
        return sky

    def _load_test(self):
        list(self._scanner.get_strings_before("endtest"))
        return None

    def _load_time(self):
        time = scnstruct.SCNTime()
        time.inital_time, time.sunset_time, time.sunrise_time = self._scanner.read_strings(3)
        return time

    def _load_trainset(self):
        self._is_trainset_opened = True

        trainset = scnstruct.SCNTrainset()

        trainset.timetable_path, trainset.track_name = self._scanner.read_strings(2)
        trainset.offset, trainset.velocity = self._scanner.read_floats(2)
        return trainset

    def _load_endtrainset(self):
        self._is_trainset_opened = False
        return scnstruct.SCNEndTrainset()