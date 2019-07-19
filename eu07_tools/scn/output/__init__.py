from eu07_tools.utils import TextWriter

def dump(elements, file):
    SCNOutput(file).dump_from_iterable(elements)
            

class SCNOutput:
    def __init__(self, file):
        self._writer = TextWriter(file)
        self._dumpers = {
            "atmo": self._dump_atmo
        }

        self._is_trainset_opened = False

    def dump_from_iterable(self, elements):
        for e in elements:
            dump = self._dumpers.get(e.typename)

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
        pass

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

    def _dump_node(self, node):
        self._writer.write_string("node")
        self._writer.write_float(node.max_distance)
        self._writer.write_float(node.min_distance)
        self._writer.write_string(node.name)

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
        
        self._writer.write("enddynamic\n")

        
            

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

    def _dump_trainset(self, trainset)
        self._writer.write_string("trainset")
        self._writer.write_string(trainset.timetable_path)
        self._writer.write_string(trainset.track_name)
        self._writer.write_float(trainset.offset)
        self._writer.write_floats(trainset.velocity)
        self._is_trainset_opened = True

    def _dump_endtrainset(self, endtrainset):
        self._writer.write_string("endtrainset\n")
        self._is_trainset_opened = False

    