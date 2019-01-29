import os

TEXTURE_EXTENSIONS = ["tga", "dds", "png", "bmp", "tex"]

def find_exisitng_textures(relpath, basedir, root, default_ext="tga"):
    relpath = _normalize_path(relpath)
    textures_root = os.path.join(root, "textures", relpath)

    lookup_paths = [
        basedir, root, textures_root
    ]

    return _find_files(relpath, lookup_paths, TEXTURE_EXTENSIONS)

def find_existing_materials(relpath, basedir, root):
    relpath = _normalize_path(relpath)
    textures_root = os.path.join(root, "textures", relpath)

    lookup_paths = [
        basedir, root, textures_root
    ]

    return _find_files(relpath, lookup_paths, ["mat"])

def find_included_file(relpath, basedir):
    pass

def _find_files(relpath, lookup_paths, extensions):
    for lookup_path in lookup_paths:
            file_path = os.path.join(lookup_path, relpath)
            
            for extension in extensions:
                full_path = os.path.join(file_path, extension)

                if os.path.exists(full_path):
                    yield full_path

def _normalize_path(path):
    path = os.path.splitext(path)[0]
    path = os.path.normpath(path.replace('\\', '/')).lstrip('/').lower()

    return path
