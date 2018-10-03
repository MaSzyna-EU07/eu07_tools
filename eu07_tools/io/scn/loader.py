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
            "firstinit": self._load_firstinit,
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

    def load_scenery_elements(self, file):
        self._token_stream = TokenStream.from_file(file)

        keyword = self._token_stream.get_token().lower()
        load_entry_func = self._entry_loaders.get(keyword)

        if load_entry_func:
            entry_type, entry_object = load_entry_func()
        else:
            raise

        yield entry_type, entry_object

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

        return "atmo", SCNAtmo(sky_color, fog_start, fog_end, fog_color, overcast)

    def _load_area(self):
        isolated_names = self._token_stream.get_tokens_before("endarea")
        return "area", isolated_names

    def _load_camera(self):
        tokens = self._token_stream.get_tokens_before("endcamera")
        values = [float(token) for token in tokens]

        position = values[:3]
        rotation = values[3:6]
        index = int(values[-1]) if len(values) == 7 else None

        return "camera", SCNCamera(position, rotation, index)

    def _load_config(self):
        self._token_stream.get_tokens_before("endconfig")

    def _load_description(self):
        self._token_stream.get_tokens_before("enddescription")

    def _load_event(self):
        self._token_stream.get_tokens_before("endevent") 

    def _load_firstinit(self):
        return "firstinit", None

    def _load_include(self):
        file_path, params = self._token_stream.get_tokens_before("end")
        return "include", IncludedFile(file_path, params)

    def _load_light(self):
        tokens = self._token_stream.get_tokens_before("endlight")
        values = [float(token) for token in tokens]

        location = values[:3]
        ambient = values[3:6]
        diffuse = values[6:9]
        specular = values[9:12]

        return "light", SCNLight(location, ambient, diffuse, specular)

    def _load_lua(self):
        file_path = self._token_stream.get_token()
        return "lua", file_path

    def _load_node(self):
        max_distance, min_distance, name, typename = self._token_stream.get_tokens(4)

        node = None
        node.max_distance = max_distance
        node.min_distance = min_distance

        return f"node::{typename}", node
        
    def _load_origin(self):
        tokens = self._token_stream.get_tokens(3)
        offset_vector = [float(token) for token in tokens]
        return "origin", Vector3(offset_vector)

    def _load_endorigin(self):
        self._token_stream.get_token()
        return "endorigin", None

    def _load_rotate(self):
        tokens = self._token_stream.get_tokens(3)
        rotation_vector = [float(token) for token in tokens]

        return "rotate", Vector3(rotation_vector)

    def _load_sky(self):
        model_path = self._token_stream.get_token()
        return "sky", model_path

    def _load_test(self):
        self._token_stream.get_tokens_before("endtest")
        
    def _load_time(self):
        tokens = self._token_stream.get_tokens_before("endtime")
        start_time, sunset_time, sunrise_time = self._token_stream.get_tokens(3)

        return SCNTime(start_time, sunset_time, sunrise_time)


class NodeLoader:
    def __init__(self, token_stream: TokenStream):
        self._token_stream = token_stream
        self._node_loaders = {
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

    def load_node(self, name: str, typename: str):
        load_node_func = self._node_loaders[typename]

        if load_node_func:
            node_object = load_node_func(name)
        else:
            node_object = None

        return node_object

    def _load_lines(self):
        color, thickness, vertices = self._load_lines()
        

    def _load_lines(self, name: str):
        lines = SCNNodeLines(name)

        tokens = self._token_stream.get_tokens(4)
        *lines.color, lines.thickness = (float(token) for token in tokens)

        tokens = self._token_stream.get_tokens_before("endlines")
        numbers = [float(token) for token in tokens]

        num_vertices = len(numbers) / 3
        vertices = []
        for vertex_id in range(num_vertices):
            vertex = numbers[vertex_id * 3:(vertex_id + 1) * 3]
            lines.add_vertex_position(vertex)

        return "lines", lines

    def _load_linestrip(self, name: str):
        return "line_strip", self._load_lines(name)

    def _load_lineloop(self, name: str):
        return "line_loop", self._load_lines(name)


    def _load_model(self, name: str):
        model = SCNNodeModel(name)

        tokens = self._token_stream.get_tokens_before("endmodel")
        *model.location, model.rotation_y = (float(token) for token in tokens[:4])
        model.file_path, model.replacableskin = tokens[4:5]

        try:
            model.light_states = (int(token) for token in tokens[6:])
        except IndexError:
            pass

        return "model", model


    