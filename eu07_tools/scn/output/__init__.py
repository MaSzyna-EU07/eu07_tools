from io import StringIO

def format_atmo(atmo):
    buffer = StringIO()

    buffer.write(
        f"atmo {atmo.color} {atmo.fog_start} {atmo.fog_end} "
    )

    if atmo.fog_end > 0:
        buffer.write(
            f"{format_sequence(atmo.fog_color)} "
        )

    buffer.write(f"{atmo.overcast} endatmo")

    return buffer.getvalue()

def format_camera(camera):
    buffer = StringIO()

    buffer.write(f"camera {format_sequence(camera.position)} {format_sequence(camera.rotation)} ")

    if camera.index != -1:
        buffer.write(f"{camera.index} ")

    buffer.write("endcamera")

    return buffer.getvalue()

def format_config(config):
    buffer = StringIO()

    buffer.write(f"//config endconfig")

    return buffer.getvalue()

def format_lua(lua):
    return f"lua {lua.path}"

def format_origin(origin):
    return f"origin {format_sequence(origin)}"

def format_endorigin(endorigin=None):
    return "endorigin"

def format_rotate(rotate):
    return f"rotate {format_sequence(rotate)}"

def format_sky(sky):
    return f"sky {sky.model_path} endsky"

def format_time(time):
    return f"time {time.initial_time} {time.sunset_time} {time.sunrise_time} endtime"

def format_trainset(trainset):
    return f"trainset {trainset.timetable_path} {trainset.track_name} {trainset.offset} {trainset.velocity}"

def format_endtrainset(endtrainset=None):
    return "endtrainset"


def format_node_triangles(node_triangles):
    buffer = StringIO()

    if node_triangles.material:
        buffer.write(
            f"material"
            f"ambient: {format_sequence(node_triangles.material.ambient)} "
            f"diffuse: {format_sequence(node_triangles.material.diffuse)} "
            f"specular: {format_sequence(node_triangles.material.specular)} "
            f"endmaterial "
        )

    buffer.write(node_triangles.map + "\n")

    num_verts = len(node_triangles.vertices)

    for vertex_id, vertex in enumerate(node_triangles.vertices, start=1):
        is_last_vertex = (vertex_id == num_verts)
        endline = "\n" if is_last_vertex else " end\n"

        buffer.write(
            format_sequence(vertex) + endline
        )

    buffer.write("endtri")

    return buffer.getvalue()


def format_node_model(node_model):
    buffer = StringIO()

    buffer.write(
        f"{format_sequence(node_model.location)} {node_model.rotation_y} "
        f"{node_model.path} {node_model.map} "
    )

    if node_model.light_states:
        buffer.write(
            f"lights {format_sequence(node_model.light_states)} "
        )

    if node_model.light_colors:
        buffer.write(
            f"lightcolors {format_sequence(node_model.light_colors)} "
        )

    buffer.write("endmodel")

    return buffer.getvalue()


def format_include(include):
    buffer = StringIO()

    buffer.write(f"include {include.path} {format_sequence(include.parameters)} end")

    return buffer.getvalue()

def format_firstinit(firstinit):
    return "FirstInit"
    

def format_sequence(seq):
    return " ".join(str(el) for el in seq)