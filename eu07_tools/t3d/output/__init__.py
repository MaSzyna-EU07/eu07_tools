from .output import T3DOutput

def dump(file, elements):
    out = T3DOutput.to_file(file)
    out.dump_from_iterable(elements)
