def dump(elements, file):
    for e in elements:
        if e.typename == "atmo":
            pass
        if e.typename == "include":
            file.write(
                f"include {e.path} {' '.join(e.parameters)} end\n"
            )