from eu07_tools.io.utils import TokenStream

class SCNLoader:
    def __init__(self):
        self._token_stream = None
        self._entry_loaders = {
            "atmo": self._load_atmo,
            "area": self._load_area,
            "camera": self._load_camera,
            "config": self._load_config,
            "description": self._load_description,
            "event": self._load_event,
            "firstinit": self._load_first_init,
            "include": self._load_include,
            "light": self._load_light,
            "lua": self._load_lua,
            "node": self._load_node,
            "origin": self._load_origin,
            "endorigin": None,
            "rotate": self._load_rotate,
            "sky": self._load_sky,
            "test": self._load_test,
            "time": self._load_time,
            "trainset": self._load_trainset
        }

    def load_scenery(self, file):
        self._token_stream = TokenStream.from_file(file)

        keyword = self._token_stream.get_token().lower()
        load_entry_func = self._entry_loaders[keyword]

        entry = load_entry_func()
        yield keyword, entry


    @property
    def progress(self):
        return self._token_stream.progress

    def _load_atmo(self):
        tokens = self._token_stream.get_tokens_before("endatmo")
        values = [float(token) for token in tokens]

        sky_color = values[:3]
        fog_start, fog_end = values[3:5]
        fog_color = values[5:8] if fog_end > 0 else None
        overcast = values[-1]

        return SCNAtmo(sky_color, fog_start, fog_end, fog_color, overcast)

    def _load_camera(self):
        tokens = self._token_stream.get_tokens_before("endcamera")
        values = [float(token) for token in tokens]

        position = values[:3]
        rotation = values[3:6]
        index = int(values[-1]) if len(values) == 7 else None

        return SCNCamera(position, rotation, index)

    def _load_config(self):
        pass

    def _load_description(self):
        pass
        #return self._token_stream.get_tokens_before("enddescription")

    def _load_event(self):
        pass

    def _load_firstinit(self):
        return None

    def _load_include(self):
        file_path, params = self._token_stream.get_tokens_before("end")
        return IncludedFile(file_path, params)

    def _load_light(self):
        tokens = self._token_stream.get_tokens_before("endlight")
        values = [float(token) for token in tokens]

        location = values[:3]
        ambient = values[3:6]
        diffuse = values[6:9]
        specular = values[9:12]

        return SCNLight(location, ambient, diffuse, specular)

    def _load_lua(self):
        file_path = self._token_stream.get_token()
        return SCNLua(file_path)

    def _load_node(self):
        pass

    def _load_origin(self):
        pass

    def _load_rotate(self):
        tokens = self._token_stream.get_tokens_before("endlight")
        values = [float(token) for token in tokens]

        return Vector3(values)

    def _load_sky(self):
        model_path = self._token_stream.get_token()
        return SCNSky(model_path)

    def _load_test(self):
        self._token_stream.get_tokens_before("endtest")
        
    def _load_time(self):
        tokens = self._token_stream.get_tokens_before("endtime")
        start_time, sunset_time, sunrise_time = self._token_stream.get_tokens(3)


class NodeLoader:
    def __init__(self):
        self._subnode_loaders {
            "dynamic": self._load_dynamic,
            "eventlauncher": self._load_eventlauncher,
            "lines": self._load_lines,
            "line_strip": self._load_linestrip,
            "line_loop": self._load_lineloop,
            "memcell": self._load_memcell,
            "model": self._load_model,
            "sound": self._load_sound,
            "track": self._load_track,
            "traction": self._load_traction,
            "tractionpowersource": self._load_tractionpowersource,
            "triangles": self._load_triangles,
            "traingle_strip": self._load_trianglestrip,
            "triangle_fan": self._load_trianglefan
        }

    def load_node(self, token_stream):
        pass

    