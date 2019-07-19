from collections.abc import Iterator
import functools

from eu07_tools.utils.input import TextScanner
import eu07_tools.scn

def load(file):
    return IterativeLoader(file)

class IterativeLoader(Iterator):
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
        atmo = eu07_tools.scn.create_element("atmo")
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
        camera = eu07_tools.scn.create_element("atmo")
        camera.location = self._scanner.read_floats(3)
        camera.rotation = self._scanner.read_floats(3)

        token = self._scanner.read_string()

        if token != "endcamera":
            camera.index = int(token)

        return camera

    def _load_config(self):
        config = eu07_tools.scn.create_element("config")
        config.content = " ".join(self._scanner.get_strings_before("endconfig"))
        return config

    def _load_description(self):
        description = eu07_tools.scn.create_element("description")
        self._scanner.get_strings_before("enddescription")
        return None

    def _load_event(self):
        camera = eu07_tools.scn.create_element("event")
        self._scanner.get_strings_before("endevent")
        return None

    def _load_firstinit(self):
        return eu07_tools.scn.create_element("firstinit")

    def _load_include(self):
        include = eu07_tools.scn.create_element("include")
        include.path, *parameters = self._scanner.get_strings_before("end")
        include.parameters = parameters

        return include

    def _load_light(self):
        light = eu07_tools.scn.create_element("include")
        self._scanner.get_strings_before("endlight")
        return None

    def _load_lua(self):
        lua = eu07_tools.scn.create_element("lua")
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
        dynamic = eu07_tools.scn.create_element("node:dynamic", name)
        dynamic.base_path, dynamic.map, dynamic.mmd_path = self._scanner.read_strings(3)

        if not self._is_trainset_opened:
            dynamic.track_name = self._scanner.read_string()

        dynamic.offset = self._scanner.read_float()
        dynamic.driver_type = self._scanner.read_string()
         # TODO: Might be not good - ensure if parameters are in good order

        if self._is_trainset_opened:
            dynamic.coupling = self._scanner.read_string()
        else:
            dynamic.coupling = "3"

        dynamic.velocity = self._scanner.read_float()
    
        dynamic.load_count = self._scanner.read_float()

        if dynamic.load_count > 0:
            dynamic.load_type = self._scanner.read_string()

        token = self._scanner.read_string()

        if token != "enddynamic":
            __, dynamic.destination, __ = self._scanner.read_strings(3)

        return dynamic

    def _load_node_eventlauncher(self, name):
        launcher = eu07_tools.scn.create_element("node:eventlauncher", name)
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
        lines = self._generic_load_lines(name)
        return lines

    def _load_node_line_loop(self, name):
        lines = self._generic_load_lines(name)
        lines.subtype = "loop"
        return lines

    def _load_node_line_strip(self, name):
        lines = self._generic_load_lines(name)
        lines.subtype = "strip"
        return lines
        
    def _generic_load_lines(self, name):
        lines = eu07_tools.scn.create_element("node:lines", name)
        *lines.color, lines.thickness = self._scanner.read_floats(4)

        while True:
            token = self._scanner.read_string()

            if token == "endline":
                break
            else:
                vertex_co = [float(token)] + self._scanner.read_floats(2)
                lines.points.new(vertex_co)

        return lines

    def _load_node_memcell(self, name):
        memcell = eu07_tools.scn.create_element("node:memcell", name)
        memcell.location = self._scanner.read_floats(3)
        memcell.values[0] = self._scanner.read_string()
        memcell.values[1:] = self._scanner.read_floats(3)
        memcell.track_name = self._scanner.read_string()

        return memcell

    def _load_node_model(self, name):
        model = eu07_tools.scn.create_element("node:model", name)
        *model.location, model.rotation_y = self._scanner.read_floats(4)
        model.path, model.map = self._scanner.read_strings(2)

        #TODO: Lights
        return model

    def _load_node_sound(self, name):
        sound = eu07_tools.scn.create_element("node:sound", name)
        sound.location = self._scanner.read_floats(3)
        sound.path = self._scanner.read_string()
        self._scanner.read_string()

        return sound


    def _load_node_track(self, name):
        track = eu07_tools.scn.create_element("node:track", name)
        track.subtype = self._scanner.read_string().lower()

        track.length = self._scanner.read_float()
        track.width = self._scanner.read_float()
        track.friction = self._scanner.read_float()
        track.sound_distance = self._scanner.read_float()
        track.quality_flag = self._scanner.read_int()
        track.damage_flag = self._scanner.read_int()
        track.environment = self._scanner.read_string()
        track.is_visible = (self._scanner.read_string() == "vis")

        if track.is_visible:
            track.map1 = self._scanner.read_string()
            track.mapping_length = self._scanner.read_float()
            track.map2 = self._scanner.read_string()
            track.tex_param1 = self._scanner.read_string()
            track.tex_param2 = self._scanner.read_string()
            track.tex_param3 = self._scanner.read_string()

        track.p1 = self._scanner.read_floats(3)
        track.p1_roll = self._scanner.read_float()
        track.cv1 = self._scanner.read_floats(3)
        track.cv2 = self._scanner.read_floats(3)
        track.p2 = self._scanner.read_floats(3)
        track.p2_roll = self._scanner.read_float()
        track.radius1 = self._scanner.read_float()

        is_junction = (track.subtype in "switch cross tributary")
        if is_junction:
            track.p3 = self._scanner.read_floats(3)
            track.p3_roll = self._scanner.read_float()
            track.cv3 = self._scanner.read_floats(3)
            track.cv4 = self._scanner.read_floats(3)
            track.p4 = self._scanner.read_floats(3)
            track.p4_roll = self._scanner.read_float()
            track.radius2 = self._scanner.read_float()

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
        traction = eu07_tools.scn.create_element("node:traction", name)

        traction.powersource_name = self._scanner.read_string()
        traction.nominal_voltage = self._scanner.read_float()
        traction.max_current = self._scanner.read_float()
        traction.resistance = self._scanner.read_float()
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
        traction.wire_offset = self._scanner.read_float()
        traction.is_visible = (self._scanner.read_string() == "vis")
        
        token = self._scanner.read_string()

        if token == "parallel":
            traction.parallel_name = self._scanner.read_string()

        return traction

    def _load_node_tractionpowersource(self, name):
        power_source = eu07_tools.scn.create_element("node:tractionpowersource", name)
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
        triangles = self._generic_load_triangles(name)
        return triangles

    def _load_node_triangle_strip(self, name):
        triangles = self._generic_load_triangles(name)
        triangles.subtype = "strip"
        return triangles

    def _load_node_triangle_fan(self, name):
        triangles = self._generic_load_triangles(name)
        triangles.subtype = "fan"
        return triangles


    def _generic_load_triangles(self, name):
        triangles = eu07_tools.scn.create_element("node:triangles", name)
        token = self._scanner.read_string().lower()
        map_ = token

        if token == "material":
            triangles.material.is_used = True

            while True:
                token = self._scanner.read_string().lower()

                if token == "endmaterial":
                    break
                elif "ambient" in token:
                    triangles.material.ambient = self._scanner.read_floats(3)
                elif "diffuse" in token:
                    triangles.material.diffuse = self._scanner.read_floats(3)
                elif "specular" in token:
                    triangles.material.specular = self._scanner.read_floats(3)

            map_ = self._scanner.read_string()
            
        triangles.map = map_

        vertex_endmark = ""
        while vertex_endmark != "endtri":
            triangles.vertices.new(self._scanner.read_floats(8))
            vertex_endmark = self._scanner.read_string()
        
        return triangles

    def _load_origin(self):
        origin = eu07_tools.scn.create_element("origin")
        origin.vector = self._scanner.read_floats(3)
        return origin

    def _load_endorigin(self):
        return eu07_tools.scn.create_element("endorigin")

    def _load_rotate(self):
        rotate = eu07_tools.scn.create_element("rotate")
        rotate.vector = self._scanner.read_floats(3)
        return rotate

    def _load_sky(self):
        sky = eu07_tools.scn.create_element("sky")
        sky.model_path, __ = self._scanner.read_strings(2)
        return sky

    def _load_test(self):
        self._scanner.get_strings_before("endtest")
        return None

    def _load_time(self):
        time = eu07_tools.scn.create_element("time")
        time.inital_time, time.sunset_time, time.sunrise_time = self._scanner.read_strings(3)
        return time

    def _load_trainset(self):
        trainset = eu07_tools.scn.create_element("trainset")

        trainset.timetable_path, trainset.track_name = self._scanner.read_strings(2)
        trainset.offset, trainset.velocity = self._scanner.read_floats(2)
        self._is_trainset_opened = True
        #TODO: Assignments
        return trainset

    def _load_endtrainset(self):
        self._is_trainset_opened = False
        return eu07_tools.scn.create_element("endtrainset")