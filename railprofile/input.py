from eu07_tools.utils import TextScanner
from .structures import RailProfile


def load(file):
    return RailProfileInput(file).load()


class RailProfileInput:
    def __init__(self, file):
        self._scanner = TextScanner.from_file(file, separators=[" ", ";", ",", "\t", "{", "}"])

    def load(self, name="none"):
        points_data = []

        buffer = []
        while 1:
            try:
                value = self._scanner.read_float()
            except ValueError:
                break
            else:
                buffer.append(value)

            if len(buffer) == 5:
                points_data.append(buffer)
                buffer = []

        blade_first_index = len(points_data) // 2

        profile = RailProfile(name)

        for i, point_data in enumerate(points_data):
            if i < blade_first_index:
                profile.rail_points.new(point_data)
            else:
                profile.blade_points.new(point_data)

        return profile
