from eu07_tools.utils import VectorXYZ
from . import SCNNode

class SCNNodeTrack(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track"
        self.length = 0
        self.width = 1.435
        self.friction = 0.15
        self.sound_distance = 20
        self.quality_flag = 0
        self.damage_flag = 0
        self.environment = "flat"
        self.visible = True
        self.material1 = "none"
        self.material2 = "none"
        self.mapping_length = 4
        # TODO: Remove those params, replace with specific attributes in subclasses
        self.geometry_param1 = 0
        self.geometry_param2 = 0
        self.geometry_param3 = 0
        self.segments = (TrackSegment())
        self.velocity = 0

        self.event0 = "none"
        self.event1 = "none"
        self.event2 = "none"
        self.eventall0 = "none"
        self.eventall1 = "none"
        self.eventall2 = "none"
        self.isolated = "none"
        self.overhead = -1
        self.angle1 = 0
        self.angle2 = 0
        self.fouling1 = "none"
        self.fouling2 = "none"
        self.vradius = 0
        self.trackbed = "none"
        self.railprofile = "none"

class SCNNodeTrackNormal(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:normal"

class SCNNodeTrackSwitch(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:switch"
        self.segments = (TrackSegment(), TrackSegment())

class SCNNodeTrackRoad(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:road"

class SCNNodeTrackCross(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:cross"
        self.segments = (TrackSegment(), TrackSegment())

class SCNNodeTrackRiver(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:river"

class SCNNodeTrackTurn(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:turn"

class SCNNodeTrackTable(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:table"

class SCNNodeTrackTributary(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:tributary"
        self.segments = (TrackSegment(), TrackSegment())
    
class TrackSegment:
    def __init__(self):
        self._p1 = TrackSegmentPoint((0, 0, 0))
        self._cv1 = VectorXYZ((0, 0, 0))
        self._cv2 = VectorXYZ((0, 0, 0)) 
        self._p2 = TrackSegmentPoint((0, 0, 0))
        self.radius = 0

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, p1):
        self._p1 = TrackSegmentPoint(p1)

    @property
    def cv1(self):
        return self._cv1

    @cv1.setter
    def cv1(self, cv1):
        self._cv1 = VectorXYZ(cv1)

    @property
    def cv2(self):
        return self._cv2

    @cv2.setter
    def cv2(self, cv2):
        self._cv2 = VectorXYZ(cv2)

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, p2):
        self._p2 = TrackSegmentPoint(p2)

class TrackSegmentPoint(VectorXYZ):
    def __init__(self, values):
        super().__init__(values)
        self.roll = 0