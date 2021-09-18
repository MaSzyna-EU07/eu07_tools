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
            "origin": self._dump_origin,
            "endorigin": self._dump_endorigin,
            "rotate": self._dump_rotate,
            "sky": self._dump_sky,
            "time": self._dump_time,
            "trainset": self._dump_trainset,
            "endtrainset": self._dump_endtrainset,
            
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
            
            "event:addvalues": self._dump_event_addvalues,
            "event:copyvalues": self._dump_event_copyvalues,
            "event:getvalues": self._dump_event_getvalues,
            "event:logvalues": self._dump_event_logvalues,
            "event:putvalues": self._dump_event_putvalues,
            "event:updatevalues": self._dump_event_updatevalues,
            "event:animation": self._dump_event_animation,
            "event:lights": self._dump_event_lights,
            "event:trackvel": self._dump_event_trackvel,
            "event:visible": self._dump_event_visible,
            "event:voltage": self._dump_event_voltage,
            "event:whois": self._dump_event_whois,
            "event:friction": self._dump_event_friction,
            "event:multiple": self._dump_event_multiple,
            "event:switch": self._dump_event_switch,
            "event:sound": self._dump_event_sound,
            "event:disable": self._dump_event_disable,
            "event:dynvel": self._dump_event_dynvel,
            "event:message": self._dump_event_message,
            "event:texture": self._dump_event_texture,
        }

        self._is_trainset_opened = False

    def dump_from_iterable(self, elements):
        for e in elements:
            dump = self._dumpers.get(e.type)

            if dump is not None:
                dump(e)
                

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
        self._writer.write_string("\nFirstInit\n\n")

    def _dump_include(self, include):
        self._writer.write_string("include")
        self._writer.write_string(include.path)
        self._writer.write_strings(include.parameters)
        self._writer.write_string("end\n")

    def _dump_lua(self, lua):
        self._writer.write_string(f"lua {lua.path}\n")

    def _dump_origin(self, origin):
        self._writer.write_string("origin")
        self._writer.write_floats(origin.vector)
        self._writer.write_string("\n")

    def _dump_endorigin(self, endorigin):
        self._writer.write_string("endorigin\n")

    def _dump_rotate(self, rotate):
        self._writer.write_string("rotate")
        self._writer.write_floats(rotate.vector)
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
        self._writer.write_float(trainset.velocity)
        self._writer.write_string("\n")
        self._is_trainset_opened = True

    def _dump_endtrainset(self, endtrainset):
        self._writer.write_string("endtrainset\n\n")
        self._is_trainset_opened = False

    def _node_dump_header(self, node):
        self._writer.write_string("node")
        self._writer.write_float(node.max_distance)
        self._writer.write_float(node.min_distance)
        self._writer.write_string(node.name)

    def _dump_node_dynamic(self, dynamic):
        self._node_dump_header(dynamic)
        self._writer.write_string("dynamic")
        self._writer.write_string(dynamic.base_path)
        self._writer.write_string(dynamic.map)
        self._writer.write_string(dynamic.mmd_path)

        if not self._is_trainset_opened:
            self._writer.write_string(dynamic.track_name)

        self._writer.write_float(dynamic.offset)
        self._writer.write_string(dynamic.driver_type)

        if self._is_trainset_opened:
            self._writer.write_string(dynamic.coupling)
        else:
            self._writer.write_float(dynamic.velocity)

        self._writer.write_float(dynamic.load_count)

        if dynamic.load_count > 0:
            self._writer.write_string(dynamic.load_type)
        
        self._writer.write_string("enddynamic\n")

    def _dump_node_eventlauncher(self, launcher):
        self._node_dump_header(launcher)
        self._writer.write_string("eventlauncher")
        self._writer.write_floats(launcher.location)
        self._writer.write_string(launcher.key)
        self._writer.write_float(launcher.delta_time)
        self._writer.write_string(launcher.first_event_name)
        self._writer.write_string(launcher.second_event_name)

        if launcher.second_event_name == "condition":
            self._writer.write_string(launcher.memcell_name)
            self._writer.write_strings(launcher.memcompare_values)

        self._writer.write_string("end\n")

    def _dump_node_lines(self, lines):
        self._node_dump_header(lines)
        if lines.subtype == "normal":
            type_ = "lines"
        elif lines.subtype == "loop":
            type_ = "line_loop"
        elif lines.subtype == "strip":
            type_ = "line_strip"

        self._writer.write_string(type_)
        self._writer.write_floats(lines.color)
        self._writer.write_float(lines.thickness)

        num_verts = len(lines.points)
        for vertex_id, vertex in enumerate(lines.points):
            self._writer.write_floats(vertex)

            endtag = "end\n" if vertex_id < (num_verts - 1) else "\nendline\n\n" 
            self._writer.write_string(endtag)

    def _dump_node_memcell(self, memcell):
        self._node_dump_header(memcell)
        self._writer.write_string("memcell")
        self._writer.write_floats(memcell.location)
        self._writer.write_string(memcell.values[0])
        self._writer.write_strings(memcell.values[1:])
        self._writer.write_string(memcell.track_name)
        self._writer.write_string("endmemcell\n")

    def _dump_node_model(self, model):
        self._node_dump_header(model)
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
        self._node_dump_header(sound)
        self._writer.write_string("sound")
        self._writer.write_floats(sound.location)
        self._writer.write_string(sound.path)
        self._writer.write_string("endsound\n")

    def _dump_node_track(self, track):
        self._node_dump_header(track)
        self._writer.write_string("track")
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
            self._writer.write_floats(track.geometry_params)
            self._writer.write_string("\n")

        self._writer.write_floats(track.p1)
        self._writer.write_float(track.p1_roll)
        self._writer.write_string("  //point 1\n")
        self._writer.write_floats(track.cv1)
        self._writer.write_string("  //control vector 1\n")
        self._writer.write_floats(track.cv2)
        self._writer.write_string("  //control vector 2\n")
        self._writer.write_floats(track.p2)
        self._writer.write_float(track.p2_roll)
        self._writer.write_string("  //point2\n")
        self._writer.write_float(track.radius1)
        self._writer.write_string("\n")

        if track.is_junction:
            self._writer.write_floats(track.p3)
            self._writer.write_float(track.p3_roll)
            self._writer.write_string("  //point3\n")
            self._writer.write_floats(track.cv3)
            self._writer.write_string("  //control vector 3\n")
            self._writer.write_floats(track.cv4)
            self._writer.write_string("  // control vector 4\n")
            self._writer.write_floats(track.p4)
            self._writer.write_float(track.p4_roll)
            self._writer.write_string("  //point4\n")
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
            self._writer.write_string("overhead")
            self._writer.write_int(track.overhead)
            self._writer.write_string("\n")
        if track.angle1 != 0:
            self._writer.write_string("angle1")
            self._writer.write_float(track.angle1)
            self._writer.write_string("\n")
        if track.angle2 != 0:
            self._writer.write_string("angle2")
            self._writer.write_float(track.angle2)
            self._writer.write_string("\n")
        if track.fouling1 != "none":
            self._writer.write_string(f"fouling1 {track.fouling1}\n")
        if track.fouling2 != "none":
            self._writer.write_string(f"fouling2 {track.fouling2}\n")
        if track.vradius != 0:
            self._writer.write_string("vradius")
            self._writer.write_float(track.vradius)
            self._writer.write_string("\n")
        if track.trackbed != "none":
            self._writer.write_string(f"trackbed {track.trackbed}\n")
        if track.railprofile != "none":
            self._writer.write_string(f"railprofile {track.railprofile}\n")
        
        self._writer.write_string("endtrack\n\n")

    def _dump_node_traction(self, traction):
        self._node_dump_header(traction)
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

        self._writer.write_string("endtraction\n\n")

    def _dump_node_tractionpowersource(self, power_source):
        self._node_dump_header(power_source)
        self._writer.write_string("tractionpowersource\n")
        self._writer.write_floats(power_source.location)
        self._writer.write_string("\n")
        self._writer.write_float(power_source.nominal_voltage)
        self._writer.write_float(power_source.voltage_frequency)
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

        self._writer.write_string("end\n\n")

    def _dump_node_triangles(self, triangles):
        self._node_dump_header(triangles)
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

            endtag = "end\n" if vertex_id < (num_verts - 1) else "\nendtri\n\n" 
            self._writer.write_string(endtag)


    def _event_dump_header(self, event):
        self._writer.write_string("event")
        self._writer.write_string(event.name)
        self._writer.write_string(event.type.split(":")[1])
        self._writer.write_float(event.delay)

    def _event_dump_ending(self, event):
        if event.random_delay != 0:
            self._writer.write_string("randomdelay")
            self._writer.write_float(event.random_delay)

        self._writer.write_string("endevent\n")

    def _event_dump_conditions(self, event):
        self._writer.write_string("condition")

        conditions = event.conditions

        if conditions.use_trackfree:
            self._writer.write_string("trackfree")

        if conditions.use_trackfree:
            self._writer.write_string("trackoccupied")

        if conditions.use_propability:
            self._writer.write_string("propability")

        if conditions.use_memcompare:
            self._writer.write_string("memcompare")
            self._writer.write_strings(conditions.memcompare_values)

    def _dump_event_addvalues(self, addvalues):
        self._event_dump_header(addvalues)
        self._writer.write_string(addvalues.memcell_name)
        self._writer.write_strings(addvalues.values)
        self._event_dump_conditions(addvalues)
        self._event_dump_ending(addvalues)

    def _dump_event_copyvalues(self, copyvalues):
        self._event_dump_header(copyvalues)
        self._writer.write_string(copyvalues.target_memcell_name)
        self._writer.write_string(copyvalues.source_memcell_name)
        if (copyvalues.mask != 0):
            self._writer.write_int(copyvalues.mask)
        self._event_dump_ending(copyvalues)

    def _dump_event_getvalues(self, getvalues):
        self._event_dump_header(getvalues)
        self._writer.write_string(getvalues.memcell_name)
        self._event_dump_ending(getvalues)

    def _dump_event_logvalues(self, logvalues):
        self._event_dump_header(logvalues)
        self._writer.write_string(logvalues.memcell_name)
        self._event_dump_ending(logvalues)

    def _dump_event_putvalues(self, putvalues):
        self._event_dump_header(putvalues)
        self._writer.write_string("none")
        self._writer.write_floats(putvalues.location)
        self._writer.write_strings(putvalues.values)
        self._event_dump_ending(putvalues)

    def _dump_event_updatevalues(self, updatevalues):
        self._event_dump_header(updatevalues)
        self._writer.write_string(updatevalues.memcell_name)
        self._writer.write_strings(updatevalues.values)
        self._event_dump_conditions(updatevalues)
        self._event_dump_ending(updatevalues)

    def _dump_event_animation(self, animation):
        self._event_dump_header(animation)
        self._writer.write_string(animation.model_name)
        self._writer.write_string(animation.anim_type)
        self._writer.write_string(animation.submodel_name)
        self._writer.write_floats(animation.vector)
        self._writer.write_float(animation.speed)
        self._event_dump_ending(animation)

    def _dump_event_lights(self, lights):
        self._event_dump_header(lights)
        self._writer.write_string(lights.model_name)
        self._writer.write_ints(lights.light_states)
        self._event_dump_ending(lights)

    def _dump_event_trackvel(self, trackvel):
        self._event_dump_header(trackvel)
        self._writer.write_string(trackvel.track_name)
        self._writer.write_float(trackvel.speed)
        self._event_dump_ending(trackvel)

    def _dump_event_visible(self, visible):
        self._event_dump_header(visible)
        self._writer.write_string(visible.node_name)
        self._writer.write_int(visible.visibility)
        self._event_dump_ending(visible)

    def _dump_event_voltage(self, voltage):
        self._event_dump_header(voltage)
        self._writer.write_string(voltage.powersource_name)
        self._writer.write_float(voltage.voltage)
        self._event_dump_ending(voltage)

    def _dump_event_whois(self, whois):
        self._event_dump_header(whois)
        self._writer.write_string(whois.memcell_name)
        self._writer.write_int(whois.mask)
        self._event_dump_ending(whois)

    def _dump_event_friction(self, friction):
        self._event_dump_header(friction)
        self._writer.write_string(friction.track_name)
        self._writer.write_float(friction.friction)
        self._event_dump_ending(friction)

    def _dump_event_multiple(self, multiple):
        self._event_dump_header(multiple)
        self._writer.write_string(multiple.memcell_name)
        self._writer.write_strings(multiple.events_names)

        if multiple.else_events_names:
            self._writer.write_string("else")
            self._writer.write_strings(multiple.else_events_names)

        self._event_dump_conditions(multiple)
        self._event_dump_ending(multiple)

    def _dump_event_switch(self, switch):
        self._event_dump_header(switch)
        self._writer.write_string(switch.switch_name)
        self._writer.write_int(switch.state)

        if switch.move_rate != -1:
            self._writer.write_float(switch.move_rate)

            if (switch.move_rate_delay != -1):
                self._writer.write_float(switch.move_rate_delay)

        self._event_dump_ending(switch)

    def _dump_event_sound(self, sound):
        self._event_dump_header(sound)
        self._writer.write_string(sound.sound_name)
        self._writer.write_int(sound.play_status)

        if sound.radio_channel > 0:
            self._writer.write_int(sound.radio_channel)

        self._event_dump_ending(sound)

    def _dump_event_disable(self, disable):
        pass

    def _dump_event_dynvel(self, dynvel):
        pass

    def _dump_event_message(self, message):
        pass

    def _dump_event_texture(self, texture):
        self._event_dump_header(texture)
        self._writer.write_string("|".join(texture.models_names))
        self._writer.write_int(texture.replacableskin_index)
        self._writer.write_string(texture.material_name)
        self._writer.write_string(texture.params_memcell_name)
        self._event_dump_ending(texture)