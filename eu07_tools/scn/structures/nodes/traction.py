from . import SCNNode
from eu07_tools.utils import VectorXYZ, TypedSequenceWrapper

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
        self._p1 = VectorXYZ((0, 0, 0))
        self._p2 = VectorXYZ((0, 0, 0))
        self._p3 = VectorXYZ((0, 0, 0))
        self._p4 = VectorXYZ((0, 0, 0))
        self.min_height = 0
        self.segment_length = 0
        self.wires_type = 1
        self.wire_offset = 0
        self.visible = True
        self.parallel_name = "none"

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, p1):
        self._p1 = VectorXYZ(p1)

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, p2):
        self._p2 = VectorXYZ(p2)

    @property
    def p3(self):
        return self._p3

    @p3.setter
    def p3(self, p3):
        self._p3 = VectorXYZ(p3)

    @property
    def p4(self):
        return self._p4

    @p4.setter
    def p4(self, p4):
        self._p4 = VectorXYZ(p4)


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