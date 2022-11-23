from eu07_tools.utils import VectorXY

VARIANT_KEYS = (
    "spring", "summer", "autumn", "winter", 
    "clear", "scattered", "broken", "overcast", "rain", "snow"
)

FLOAT_KEYS = (
    "selfillum", "opacity",
)

INT_KEYS = (
    "shadow_rank",
)

STRING_KEYS = (
    "shader",
)

DEFAULT_VALUES = {
    "shader": "",
    "selfillum": -1,
    "opacity": 1,
    "size": VectorXY((-1, -1)),
    "shadow_rank": 3,
    "shader": "",
}