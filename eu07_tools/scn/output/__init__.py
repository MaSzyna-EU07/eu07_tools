from eu07_tools.utils import TextWriter

def dump(elements, file):
    SCNOutput(file).dump_from_iterable(elements)
            

class SCNOutput:
    def __init__(self, file):
        self._writer = TextWriter(file)
        self._dumpers = {
            "atmo": self._dump_atmo,
            "camera": self._dump_camera,
            "config": self._dump_config,
            "event": self._dump_event,
            "firstinit": self._dump_firstinit,
            "include": self._dump_include,
            "lua": self._dump_lua,
            "node": self._dump_node,
            "origin": self._dump_origin,
            "endorigin": self._dump_endorigin,
            "rotate": self._dump_rotate,
            "trainset": self._dump_trainset,
            "endtrainset": self._dump_endtrainset
        }

        self._node_dumpers = {
            "node:dynamic": self._dump_node_dynamic,
            "node:eventlauncher": self._dump_node_eventlauncher,
            "node:lines": self._dump_node_lines,
            "node:memcell": self._dump_node_memcell,
            "node:model": self._dump_node_model,
            "node:sound": self._dump_node_sound,
            "node:track": self._dump_node_track,
            "node:traction": self._dump_node_traction,
            "node:tractionpowersource": self._dump_node_tractionpowersource,
            "node:triangles": self._dump_node_triangles,
        }

        self._is_trainset_opened = False

    def dump_from_iterable(self, elements):
        for e in elements:
            dump = self._dumpers.get(e.typename)

            if dump is not None:
                dump(e)
                self._writer.write_string("\n")

    def _dump_atmo(self, atmo):
        self._writer.write_string("atmo")
        self._writer.write_floats(atmo.sky_color)
        self._writer.write_float(atmo.fog_start)
        self._writer.write_float(atmo.fog_end)
        
        if atmo.fog_end > 0:
            self._writer.write_floats(atmo.fog_color)

        self._writer.write_float(atmo.overcast)
        self._writer.write_string("endatmo\n")

    def _dump_camera(self, camera):
        self._writer.write_string("camera")
        self._writer.write_floats(camera.location)
        self._writer.write_floats(camera.rotation)
        
        if camera.index != -1:
            self._writer.write_int(camera.index)

        self._writer.write_string("endcamera\n")

    def _dump_config(self, config):
        self._writer.write_string(f"config {config.content} endconfig\n")

    def _dump_event(self, event):
        pass

    def _dump_firstinit(self, firstinit):
        self._writer.write_string("FirstInit\n")

    def _dump_include(self, include):
        self._writer.write_string("include")
        self._writer.write_string(include.path)
        self._writer.write_strings(include.parameters)
        self._writer.write_string("end\n")

    def _dump_lua(self, lua):
        self._writer.write_string(f"lua {lua.path}\n")

    def _dump_origin(self, origin):
        self._writer.write_string("origin")
        self._writer.write_floats(origin)
        self._writer.write_string("\n")

    def _dump_endorigin(self, endorigin):
        self._writer.write_string("endorigin\n")

    def _dump_rotate(self, rotate):
        self._writer.write_string("rotate")
        self._writer.write_floats(rotate)
        self._writer.write_string("\n")

    def _dump_sky(self, sky):
        self._writer.write_string(f"sky {sky.model_path} endsky\n")

    def _dump_time(self, time):
        self._writer.write_string("time")
        self._writer.write_string(time.initial_time)
        self._writer.write_string(time.sunset_time)
        self._writer.write_string(time.sunrise_time)
        self._writer.write_string("endtime\n")

    def _dump_trainset(self, trainset):
        self._writer.write_string("trainset")
        self._writer.write_string(trainset.timetable_path)
        self._writer.write_string(trainset.track_name)
        self._writer.write_float(trainset.offset)
        self._writer.write_floats(trainset.velocity)
        self._is_trainset_opened = True

    def _dump_endtrainset(self, endtrainset):
        self._writer.write_string("endtrainset\n")
        self._is_trainset_opened = False

    def _dump_node(self, node):
        self._writer.write_string("node")
        self._writer.write_float(node.max_distance)
        self._writer.write_float(node.min_distance)
        self._writer.write_string(node.name)

        node_dump = self._node_dumpers.get(node.typename)
        if node_dump is not None:
            node_dump(node)

    def _dump_node_dynamic(self, dynamic):
        # TODO: Might be not good - ensure if parameters are in good order
        self._writer.write_string(dynamic.base_path)
        self._writer.write_string(dynamic.map)
        self._writer.write_string(dynamic.mmd_path)

        if not self._is_trainset_opened:
            self._writer.write_string(dynamic.track_name)

        self._writer.write_float(dynamic.offset)

        if self._is_trainset_opened:
            self._writer.write_string(dynamic.coupling)
        else:
            self._writer.write_float(dynamic.velocity)

        self._writer.write_float(dynamic.load_count)

        if dynamic.load_count > 0:
            self._writer.write_string(dynamic.load_type)

        if dynamic.destination != "none":
            self._writer.write_string(f"destination {dynamic.destination}")
        
        self._writer.write_string("enddynamic\n")

    def _dump_node_eventlauncher(self, launcher):
        self._writer.write_string("eventlauncher")
        self._writer.write_floats(launcher.location)
        self._writer.write_float(launcher.rotation)
        self._writer.write_string(launcher.key)
        self._writer.write_float(launcher.delta_time)
        self._writer.write_string(launcher.first_event_name)
        self._writer.write_string(launcher.second_event_name)

        if launcher.second_event_name == "condition":
            self._writer.write_string(launcher.memcell_name)
            self._writer.write_int(launcher.check_mask)

        self._writer.write_string("end\n")

    def _dump_node_lines(self, lines):
        if lines.subtype == "normal":
            type_ = "lines"
        elif lines.subtype == "loop":
            type_ = "line_loop"
        elif lines.subtype == "strip":
            type_ = "line_strip"

        self._writer.write_string(type_)
        self._writer.write_floats(lines.color)
        self._writer.write_float(lines.thickness)

        num_verts = len(lines.vertices)
        for vertex_id, vertex in enumerate(lines.vertices):
            self._writer.write_floats(vertex)

            endtag = "end\n" if vertex_id < (num_verts - 1) else "\nendline\n" 
            self._writer.write_string(endtag)

    def _dump_node_memcell(self, memcell):
        self._writer.write_string("memcell")
        self._writer.write_floats(memcell.location)
        self._writer.write_string(memcell.values[0])
        self._writer.write_floats(memcell.values[1:])
        self._writer.write_string(memcell.track_name)
        self._writer.write_string("endmemcell\n")

    def _dump_node_model(self, model):
        self._writer.write_string("model")
        self._writer.write_floats(model.location)
        self._writer.write_float(model.rotation_y)
        self._writer.write_string(model.path)
        self._writer.write_string(model.map)

        if model.light_states:
            self._writer.write_string("lights")
            if model.light_states:
                self._writer.write_floats(model.light_states)

            if model.light_colors:
                self._writer.write_string("lightcolors")
                for color in model.light_colors:
                    self._writer.write_string(color)

        self._writer.write_string("endmodel\n")

    def _dump_node_sound(self, sound):
        self._writer.write_string("sound")
        self._writer.write_floats(sound.location)
        self._writer.write_string(sound.path)
        self._writer.write_string("endsound")

    def _dump_node_track(self, track):
        self._writer.write_string(track.subtype)
        self._writer.write_float(track.length)
        self._writer.write_float(track.width)
        self._writer.write_float(track.friction)
        self._writer.write_float(track.sound_distance)
        self._writer.write_int(track.quality_flag)
        self._writer.write_int(track.damage_flag)
        self._writer.write_string(track.environment)
        self._writer.write_string("vis\n" if track.is_visible else "unvis\n")

        if track.is_visible:
            self._writer.write_string(track.map1)
            self._writer.write_float(track.mapping_length)
            self._writer.write_string(track.map2)
            self._writer.write_float(track.tex_param1)
            self._writer.write_float(track.tex_param2)
            self._writer.write_float(track.tex_param3)
            self._writer.write_string("\n")

        self._writer.write_floats(track.p1)
        self._writer.write_float(track.p1_roll)
        self._writer.write_string("\n")
        self._writer.write_floats(track.cv1)
        self._writer.write_string("\n")
        self._writer.write_floats(track.cv2)
        self._writer.write_string("\n")
        self._writer.write_floats(track.p2)
        self._writer.write_float(track.p2_roll)
        self._writer.write_string("\n")
        self._writer.write_float(track.radius1)
        self._writer.write_string("\n")

        if track.subtype in "switch cross tributary":
            self._writer.write_floats(track.p3)
            self._writer.write_float(track.p3_roll)
            self._writer.write_string("\n")
            self._writer.write_floats(track.cv3)
            self._writer.write_string("\n")
            self._writer.write_floats(track.cv4)
            self._writer.write_string("\n")
            self._writer.write_floats(track.p4)
            self._writer.write_float(track.p4_roll)
            self._writer.write_string("\n")
            self._writer.write_float(track.radius2)
            self._writer.write_string("\n")

        if track.event0 != "none":
            self._writer.write_string(f"event0 {track.event0}\n")
        if track.event1 != "none":
            self._writer.write_string(f"event1 {track.event1}\n")
        if track.event2 != "none":
            self._writer.write_string(f"event2 {track.event2}\n")
        if track.eventall0 != "none":
            self._writer.write_string(f"eventall0 {track.eventall0}\n")
        if track.eventall1 != "none":
            self._writer.write_string(f"eventall1 {track.eventall1}\n")
        if track.eventall2 != "none":
            self._writer.write_string(f"eventall2 {track.eventall2}\n")
        if track.isolated != "none":
            self._writer.write_string(f"isolated {track.isolated}\n")
        if track.overhead != -1:
            self._writer.write_int(f"overhead {track.overhead}\n")
        if track.angle1 != 0:
            self._writer.write_float(f"angle1 {track.angle1}\n")
        if track.angle2 != 0:
            self._writer.write_float(f"angle2 {track.angle2}\n")
        if track.fouling1 != "none":
            self._writer.write_string(f"fouling1 {track.fouling1}\n")
        if track.fouling2 != "none":
            self._writer.write_string(f"fouling2 {track.fouling2}\n")
        if track.vradius != 0:
            self._writer.write_float(f"vradius {track.vradius}\n")
        if track.trackbed != "none":
            self._writer.write_string(f"trackbed {track.trackbed}\n")
        if track.railprofile != "none":
            self._writer.write_string(f"railprofile {track.railprofile}\n")
        
        self._writer.write_string("endtrack\n")

    def _dump_node_traction(self, traction):
        self._writer.write_string("traction")
        self._writer.write_string(traction.powersource_name)
        self._writer.write_float(traction.nominal_voltage)
        self._writer.write_float(traction.max_current)
        self._writer.write_float(traction.resistance)
        self._writer.write_string(traction.wire_material_type)
        self._writer.write_float(traction.wire_thickness)
        self._writer.write_int(traction.damage_flag)
        self._writer.write_string("\n")
        self._writer.write_floats(traction.p1)
        self._writer.write_string("\n")
        self._writer.write_floats(traction.p2)
        self._writer.write_string("\n")
        self._writer.write_floats(traction.p3)
        self._writer.write_string("\n")
        self._writer.write_floats(traction.p4)
        self._writer.write_string("\n")
        self._writer.write_float(traction.min_height)
        self._writer.write_float(traction.segment_length)
        self._writer.write_int(traction.wires_type)
        self._writer.write_float(traction.wire_offset)

        self._writer.write_string("vis\n" if traction.is_visible else "unvis\n")

        if traction.parallel_name != "none":
            self._writer.write_string(f"parallel {traction.parallel_name}\n")

        self._writer.write_string("endtraction\n")

    def _dump_node_tractionpowersource(self, power_source):
        self._writer.write_string("tractionpowersource\n")
        self._writer.write_floats(power_source.location)
        self._writer.write_string("\n")
        self._writer.write_float(power_source.nominal_voltage)
        self._writer.write_floats(power_source.voltage_frequency)
        self._writer.write_float(power_source.internal_resistance)
        self._writer.write_float(power_source.max_output_current)
        self._writer.write_string("\n")
        self._writer.write_float(power_source.fast_fuse_timeout)
        self._writer.write_int(power_source.fast_fuse_repetition)
        self._writer.write_float(power_source.slow_fuse_timeout)
        self._writer.write_string("\n")

        if power_source.recuperation:
            self._writer.write_string("recuperation\n")
        if power_source.section:
            self._writer.write_string("section\n")

        self._writer.write_string("end\n")

    def _dump_node_triangles(self, triangles):
        if triangles.subtype == "normal":
            type_ = "triangles"
        elif triangles.subtype == "fan":
            type_ = "triangle_fan"
        elif triangles.subtype == "strip":
            type_ = "triangle_strip"

        self._writer.write_string(type_)

        if triangles.material.is_used:
            self._writer.write_string("material")
            if triangles.material.ambient:
                self._writer.write_string("ambient:")
                self._writer.write_floats(triangles.material.ambient)
            if triangles.material.diffuse:
                self._writer.write_string("diffuse:")
                self._writer.write_floats(triangles.material.diffuse)
            if triangles.material.specular:
                self._writer.write_string("specular:")
                self._writer.write_floats(triangles.material.specular)
            self._writer.write_string("endmaterial")
        
        self._writer.write_string(triangles.map + "\n")

        num_verts = len(triangles.vertices)
        for vertex_id, vertex in enumerate(triangles.vertices):
            self._writer.write_floats(vertex)

            endtag = "end\n" if vertex_id < (num_verts - 1) else "\nendtri\n" 
            self._writer.write_string(endtag)



    