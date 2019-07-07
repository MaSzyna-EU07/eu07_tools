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
        self.tex_param1 = 0
        self.tex_param2 = 0
        self.tex_param3 = 0
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
    
class TrackSegment:
    def __init__(self):
        self.p1 = TrackSegmentPoint()
        self.cv1 = VectorXYZ((0, 0, 0))
        self.cv2 = VectorXYZ((0, 0, 0)) 
        self.p2 = TrackSegmentPoint()
        self.radius = 0

class TrackSegmentPoint(VectorXYZ):
    def __init__(self):
        super().__init__()
        self.roll = 0