NESTED_MAPPING_KEYS = {
    "spring", "summer", "autumn", "winter", 
    "rain", "snow", "cloudy", "clear"
}

NUMERIC_KEYS = {
    "selfillum", "opacity"
}

STRING_KEYS = {
    "shader",
}


def get_texture_index_from_key(key):
    part2 = key.replace("texture", "")
    if part2 == "_diffuse":
        return 1
    elif part2 == "_normalmap":
        return 2
    else:
        return int(part2)


def get_alias_from_key(key):
    part2 = key.replace("texture", "")
    if part2.startswith("_"):
        return part2.lstrip("_")

    return ""