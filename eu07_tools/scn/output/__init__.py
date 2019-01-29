from io import StringIO

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