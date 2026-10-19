from collections.abc import Iterator
import functools

from ..utils.input import TextScanner
from .structures import create_element

def load(file, tokenizer=None):
    return SCNInput(file, tokenizer)

class SCNInput(Iterator):
    def __init__(self, file, tokenizer=None):
        self._scanner = TextScanner.from_file(file, tokenizer)
        self._iterator = self._load()
        self._file = file

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
            "eventlauncher": self._load_node_eventlauncher,
            "lines": self._load_node_lines,
            "line_strip": self._load_node_line_strip,
            "line_loop": self._load_node_line_loop,
            "memcell": self._load_node_memcell,
            "model": self._load_node_model,
            "sound": self._load_node_sound,
            "track": self._load_node_track,
            "traction": self._load_node_traction,
            "tractionpowersource": self._load_node_tractionpowersource,
            "triangles": self._load_node_triangles,
            "triangle_strip": self._load_node_triangle_strip,
            "triangle_fan": self._load_node_triangle_fan,
        }

        self._event_loaders = {
            "addvalues": self._load_event_addvalues,
            "copyvalues": self._load_event_copyvalues,
            "getvalues": self._load_event_getvalues,
            "logvalues": self._load_event_logvalues,
            #"putvalues": self._load_event_putvalues,
            "updatevalues": self._load_event_updatevalues,
            "animation": self._load_event_animation,
            "lights": self._load_event_lights,
            "trackvel": self._load_event_trackvel,
            "visible": self._load_event_visible,
            "voltage": self._load_event_voltage,
            "whois": self._load_event_whois,
            "friction": self._load_event_friction,
            "multiple": self._load_event_multiple,
            "switch": self._load_event_switch,
            "sound": self._load_event_sound,
            "disable": self._load_event_disable,
            "dynvel": self._load_event_dynvel,
            "message": self._load_event_message,
            "texture": self._load_event_texture,
        }

        self._is_trainset_open = False


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
                try:
                    element = load_element()
                except ValueError as e:
                    raise Warning(f"Bad SCN syntax in file: {self._scanner.filename} in line: {self._scanner.line_number}")
                if element:
                    yield element


    def _load_atmo(self):
        atmo = create_element("atmo")
        atmo.sky_color = self._scanner.read_floats(3)
        atmo.fog_start = self._scanner.read_float()
        atmo.fog_end = self._scanner.read_float()
        
        if atmo.fog_end > 0:
            atmo.fog_color = self._scanner.read_floats(3)

        token = self._scanner.read_string().lower()

        if token != "endatmo":
            atmo.overcast = float(token)
            self._scanner.read_string() # endtag

        return atmo


    def _load_camera(self):
        camera = create_element("camera")
        camera.location = self._scanner.read_floats(3)
        camera.rotation = self._scanner.read_floats(3)

        token = self._scanner.read_string()

        if token != "endcamera":
            camera.index = int(token)
            self._scanner.read_string() # endtag

        return camera

    def _load_config(self):
        config = create_element("config")
        config.content = " ".join(self._scanner.read_strings_before("endconfig"))
        return config

    def _load_description(self):
        description = create_element("description")
        self._scanner.read_strings_before("enddescription")
        return None

    def _load_event(self):
        event = create_element("event")
        self._scanner.read_strings_before("endevent")
        return None

    def _load_firstinit(self):
        return create_element("firstinit")

    def _load_include(self):
        include = create_element("include")
        include.path, *parameters = self._scanner.read_strings_before("end")
        include.parameters = parameters

        return include

    def _load_light(self):
        light = create_element("light")
        self._scanner.read_strings_before("endlight")
        return None

    def _load_lua(self):
        lua = create_element("lua")
        lua.path = self._scanner.read_string()
        return lua

    def _load_origin(self):
        origin = create_element("origin")
        origin.vector = self._scanner.read_floats(3)
        return origin

    def _load_endorigin(self):
        return create_element("endorigin")

    def _load_rotate(self):
        rotate = create_element("rotate")
        rotate.vector = self._scanner.read_floats(3)
        return rotate

    def _load_sky(self):
        sky = create_element("sky")
        sky.model_path, __ = self._scanner.read_strings(2)
        return sky

    def _load_test(self):
        self._scanner.read_strings_before("endtest")
        return None

    def _load_time(self):
        time = create_element("time")
        time.inital_time, time.sunset_time, time.sunrise_time = self._scanner.read_strings(3)
        self._scanner.read_string() # endtag
        return time

    def _load_trainset(self):
        trainset = create_element("trainset")

        trainset.timetable_path, trainset.track_name = self._scanner.read_strings(2)
        trainset.offset, trainset.velocity = self._scanner.read_floats(2)
        self._is_trainset_open = True
        #TODO: Assignments
        return trainset

    def _load_endtrainset(self):
        self._is_trainset_open = False
        return create_element("endtrainset")

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
        dynamic = create_element("node:dynamic", name)
        dynamic.base_path, dynamic.map, dynamic.mmd_path = self._scanner.read_strings(3)

        if not self._is_trainset_open:
            dynamic.track_name = self._scanner.read_string()

        dynamic.offset = self._scanner.read_float()
        dynamic.driver_type = self._scanner.read_string().lower()
        
        dynamic.coupling = (
            self._scanner.read_string() if self._is_trainset_open
            else "3"
        )

        if not self._is_trainset_open:
            dynamic.velocity = self._scanner.read_float()
    
        dynamic.load_count = self._scanner.read_float()

        if dynamic.load_count:
            dynamic.load_type = self._scanner.read_string()

            if dynamic.load_type == "enddynamic":
                dynamic.load_count = 0
                dynamic.load_type = "none"
                return dynamic
        
        self._scanner.read_string() # endtag

        return dynamic

    def _load_node_eventlauncher(self, name):
        launcher = create_element("node:eventlauncher", name)
        *launcher.location, launcher.radius = self._scanner.read_floats(4)
        launcher.key = self._scanner.read_string()
        launcher.delta_time = self._scanner.read_float()
        launcher.first_event_name, launcher.second_event_name = self._scanner.read_strings(2)

        if launcher.second_event_name == "condition":
            launcher.memcell_name = self._scanner.read_string()
            launcher.memcompare_values = self._scanner.read_strings(3)
        
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
        lines = create_element("node:lines", name)
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
        memcell = create_element("node:memcell", name)
        memcell.location = self._scanner.read_floats(3)
        memcell.values = self._scanner.read_strings(3)
        memcell.track_name = self._scanner.read_string()
        self._scanner.read_string()

        return memcell

    def _load_node_model(self, name):
        model = create_element("node:model", name)
        *model.location, model.rotation.y = self._scanner.read_floats(4)
        model.path, model.map = self._scanner.read_strings(2)


        additional_tokens = self._scanner.read_strings_before("endmodel")

        if "notransition" in additional_tokens:
            model.notransition = True

        try:
            angles_index = additional_tokens.index("angles")
            model.rotation = [float(token) for token in additional_tokens[angles_index + 1: angles_index + 4]]
        except ValueError:
            pass

        try:
            lights_index = additional_tokens.index("lights")
            counter = 0
            while True:
                token = additional_tokens[lights_index + counter]

                try:
                    model.light_states.append(float(token))
                except ValueError:
                    break

                counter += 1

        except ValueError:
            pass

        try:
            lightcolors_index = additional_tokens.index("lightcolors")
            counter = 0
            while True:
                token = additional_tokens[lightcolors_index + counter]

                try:
                    model.light_colors.append(float(token))
                except ValueError:
                    break

                counter += 1

        except ValueError:
            pass

        return model

    def _load_node_sound(self, name):
        sound = create_element("node:sound", name)
        sound.location = self._scanner.read_floats(3)
        sound.path = self._scanner.read_string()
        self._scanner.read_string() # endtag

        return sound


    def _load_node_track(self, name):
        track = create_element("node:track", name)
        track.subtype = self._scanner.read_string().lower()

        track.length = self._scanner.read_float()
        track.width = self._scanner.read_float()
        track.friction = self._scanner.read_float()
        track.sound_distance = self._scanner.read_float()
        track.quality_flag = self._scanner.read_int()
        track.damage_flag = self._scanner.read_int()
        track.environment = self._scanner.read_string().lower()
        if (track.environment == "mountain"): 
            track.environment = "mountains"
        track.is_visible = (self._scanner.read_string().lower() == "vis")

        if track.is_visible:
            track.map1 = self._scanner.read_string()
            track.mapping_length = self._scanner.read_float()
            track.map2 = self._scanner.read_string()
            track.geometry_params = self._scanner.read_floats(3)

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
        traction = create_element("node:traction", name)

        traction.powersource_name = self._scanner.read_string()
        traction.nominal_voltage = self._scanner.read_float()
        traction.max_current = self._scanner.read_float()
        traction.resistance = self._scanner.read_float()
        traction.wire_material_type = self._scanner.read_string().lower()
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
        traction.is_visible = (self._scanner.read_string().lower() == "vis")
        
        token = self._scanner.read_string()

        if token == "parallel":
            traction.parallel_name = self._scanner.read_string()
            self._scanner.read_string() # endtag

        return traction

    def _load_node_tractionpowersource(self, name):
        power_source = create_element("node:tractionpowersource", name)
        power_source.location = self._scanner.read_floats(3)
        power_source.nominal_voltage = self._scanner.read_float()
        power_source.voltage_frequency = self._scanner.read_float()
        power_source.internal_resistance = self._scanner.read_float()
        power_source.max_output_current = self._scanner.read_float()
        power_source.fast_fuse_timeout = self._scanner.read_float()
        power_source.fast_fuse_repetition = self._scanner.read_int()
        power_source.slow_fuse_timeout = self._scanner.read_float()

        optional = [x.lower() for x in self._scanner.read_strings_before("end")]

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
        triangles = create_element("node:triangles", name)
        token = self._scanner.read_string()
        map_ = token

        if token.lower() == "material":
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
            triangles.geometry.vertices.new(self._scanner.read_floats(8))
            vertex_endmark = self._scanner.read_string()
        
        return triangles


    def _load_event(self):
        name, subtype = self._scanner.read_strings(2)
        delay = self._scanner.read_float()

        load_event = self._event_loaders.get(subtype)

        if load_event:
            event = load_event(name)
            event.delay = delay

            token = self._scanner.read_string()
            if (token == "randomdelay"):
                event.random_delay = self._scanner.read_float()
                self._scanner.read_string()

            return event


    def _events_load_conditions(self, conditions):
        token = self._scanner.read_string()

        if (token == "trackoccupied"):
            conditions.use_trackoccupied = True

        if (token == "trackfree"):
            conditions.use_trackfree = True

        if (token == "propability"):
            conditions.use_propability = True

        if (token == "memcompare"):
            conditions.use_memcompare = True
            conditions.memcompare_values = self._scanner.read_strings(3)


    def _load_event_addvalues(self, name):
        addvalues = create_element("event:addvalues", name)

        addvalues.memcell_name = self._scanner.read_string()
        addvalues.values = self._scanner.read_strings(3)

        token = self._scanner.read_string()

        if (token == "condition"):
            self._events_load_conditions(addvalues.conditions)

        return addvalues


    def _load_event_copyvalues(self, name):
        copyvalues = create_element("event:copyvalues", name)

        copyvalues.target_memcell_name = self._scanner.read_string()
        copyvalues.source_memcell_name = self._scanner.read_string()
        token = self._scanner.read_string()
        if token not in "endevent randomdelay":
            copyvalues.mask = int(token)
        else:
            self._scanner.put_back(token)

        return copyvalues

    
    def _load_event_getvalues(self, name):
        getvalues = create_element("event:getvalues", name)

        getvalues.memcell_name = self._scanner.read_string()

        return getvalues


    def _load_event_logvalues(self, name):
        logvalues = create_element("event:logvalues", name)

        logvalues.memcell_name = self._scanner.read_string()

        return logvalues


    def _load_event_putvalues(self, name):
        putvalues = create_element("event:putvalues", name)
        self._scanner.read_string() # "none"
        putvalues.location = self._scanner.read_floats(3)
        putvalues.values = self._scanner.read_strings(3)
        return putvalues


    def _load_event_updatevalues(self, name):
        updatevalues = create_element("event:updatevalues", name)

        updatevalues.memcell_name = self._scanner.read_string()
        updatevalues.values = self._scanner.read_strings(3)

        token = self._scanner.read_string()

        if (token == "condition"):
            self._events_load_conditions(updatevalues.conditions)
        else:
            self._scanner.put_back(token)

        return updatevalues
       

    def _load_event_animation(self, name):
        animation = create_element("event:animation", name)

        animation.model_name, animation.anim_type, animation.submodel_name = self._scanner.read_strings(3)
        *animation.vector, animation.delay = self._scanner.read_floats(4)

        return animation
    

    def _load_event_lights(self, name):
        lights = create_element("event:lights", name)

        lights.model_name = self._scanner.read_string()
        while True:
            token = self._scanner.read_string()
            if (token in "endevent randomdelay"):
                self._scanner.put_back(token)
                break

            lights.light_states.append(float(token))

        return lights

    
    def _load_event_trackvel(self, name):
        trackvel = create_element("event:trackvel", name)

        trackvel.track_name = self._scanner.read_string()
        trackvel.velocity = self._scanner.read_float()

        return trackvel


    def _load_event_visible(self, name):
        visible = create_element("event:visible", name)

        visible.node_name = self._scanner.read_string()
        visible.visibility = self._scanner.read_int() 

        return visible


    def _load_event_voltage(self, name):
        voltage = create_element("event:voltage", name)

        voltage.powersource_name = self._scanner.read_string()
        voltage.voltage = self._scanner.read_float() 

        return voltage

    
    def _load_event_whois(self, name):
        whois = create_element("event:whois", name)

        whois.memcell_name = self._scanner.read_string()
        whois.mask = self._scanner.read_int() 

        return whois


    def _load_event_friction(self, name):
        friction = create_element("event:friction", name)

        friction.track_name = self._scanner.read_string()
        friction.friction = self._scanner.read_float() 

        return friction


    def _load_event_multiple(self, name):
        multiple = create_element("event:multiple", name)

        while True:
            token = self._scanner.read_string()
            if token not in "condition else randomdelay endevent":
                break
            multiple.events_names.append(token)
            
        if (token == "else"):
            while True:
                token = self._scanner.read_string()
                if token not in "condition randomdelay endevent":
                    break
                multiple.else_events_names.append(token)
                
        if token == "condition":
            self._events_load_conditions(multiple.conditions)

        return multiple

    
    def _load_event_switch(self, name):
        switch = create_element("event:switch", name)

        switch.switch_name = self._scanner.read_string()
        switch.state = self._scanner.read_int()

        # TODO: Naprawic tego potwora jakos
        token = self._scanner.read_string()
        if token not in "endevent randomdelay":
            switch.move_rate = self._scanner.read_float()
            token = self._scanner.read_string()
            if token not in "endevent randomdelay":
                switch.move_rate_delay = self._scanner.read_float()
            else:
                self._scanner.put_back(token)
        else:
            self._scanner.put_back(token)

        return switch

    
    def _load_event_sound(self, name):
        sound = create_element("event:sound", name)

        sound.sound_name = self._scanner.read_string()
        sound.play_status = self._scanner.read_string()

        token = self._scanner.read_string()
        if (token in "endevent randomdelay"):
            self._scanner.put_back(token)
        else:
            sound.radio_channel = int(token)

        return sound


    def _load_event_disable(self, name):
        disable = create_element("event:disable", name)
        self._scanner.read_string()
        return disable


    def _load_event_dynvel(self, name):
        dynvel = create_element("event:dynvel", name)
        self._scanner.read_string()
        return dynvel


    def _load_event_message(self, name):
        message = create_element("event:message", name)
        self._scanner.read_string()
        return message


    def _load_event_texture(self, name):
        texture = create_element("event:texture", name)

        texture.models_names = self._scanner.read_string().split("|")
        texture.replacableskin_index = self._scanner.read_int()
        texture.material_name = self._scanner.read_string()
        texture.params_memcell_name = self._scanner.read_string()

        return texture