from eu07_tools.utils import VectorXY

NESTED_MAPPING_KEYS = {
    "spring", "summer", "autumn", "winter", 
    "rain", "snow", "cloudy", "clear"
}

NUMERIC_KEYS = {
    "selfillum", "opacity", "shadow_rank"
}

STRING_KEYS = {
    "shader",
}

DEFAULT_VALUES = {
    "selfillum": -1,
    "opacity": 1,
    "size": VectorXY((-1, -1)),
    "shadow_rank": 3,
}