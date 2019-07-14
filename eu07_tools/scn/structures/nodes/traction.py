from . import SCNNode
from eu07_tools.utils import VectorXYZ

class SCNNodeTraction(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:traction"
        self.powersource_name = "none"
        self.nominal_voltage = 0
        self.max_current = 0
        self.resistivity = 0
        self.wire_material_type = "Cu"
        self.wire_thickness = 1.0
        self.damage_flag = 0
        self.points = (
            VectorXYZ((0, 0, 0)), VectorXYZ((0, 0, 0)),
            VectorXYZ((0, 0, 0)), VectorXYZ((0, 0, 0))
        )
        self.min_height = 0
        self.segment_length = 0
        self.wires_type = 1
        self.wire_offset = 0
        self.visible = True
        self.parallel_name = "none"


class SCNNodeTractionPowerSource(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:tractionpowersource"
        self._location = VectorXYZ((0, 0, 0))
        self.nominal_voltage = 0
        self.voltage_frequency = 0
        self.internal_resistance = 0
        self.max_output_current = 0
        self.fast_fuse_timeout = 0
        self.fast_fuse_repetition = 0
        self.slow_fuse_timeout = 0
        self.recuperation = False
        self.section = False

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)