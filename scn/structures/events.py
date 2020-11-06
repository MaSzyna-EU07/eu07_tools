from .nodes import MemcellValues
from eu07_tools.utils.structures import VectorXYZ


class Event:
    def __init__(self, name):
        self.name = name
        self.type = "event"
        self.subtype = ""
        self.delay = 0
        self.random_delay = 0


class EventAddvalues(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:addvalues"
        self.memcell_name = "none"
        self._values = MemcellValues(("*", "*", "*"))
        self.conditions = Conditions()

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = MemcellValues(values)


class EventCopyvalues(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:copyvalues"
        self.target_memcell_name = "none"
        self.source_memcell_name = "none"
        self.mask = 0


class EventGetvalues(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:getvalues"
        self.memcell_name = "none"


class EventLogvalues(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:logvalues"
        self.memcell_name = "none"


class EventPutvalues(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:putvalues"
        self._location = VectorXYZ((0, 0, 0))
        self._values = MemcellValues("none", "*", "*")

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)

    @property
    def values(self):
        return values

    @values.setter
    def values(self, values):
        self._values = MemcellValues(values)


class EventUpdatevalues(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:updatevalues"
        self.memcell_name = "none"
        self._values = MemcellValues(("*", "*", "*"))
        self.conditions = Conditions()

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = MemcellValues(values)


class EventAnimation(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:animation"
        self.model_name = "none"
        self.anim_type = "translate"
        self.submodel_name = "none"
        self._vector = VectorXYZ((0, 0, 0))
        self.speed = 0
        
    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, vector):
        self._vector = VectorXYZ(vector)


class EventLights(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:lights"
        self.model_name = "none"
        self.light_states = []
        

class EventTrackvel(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:trackvel"
        self.track_name = "none"
        self.speed = 0


class EventVisible(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:visible"
        self.node_name = "none"
        self.visibility = 1 


class EventVoltage(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:voltage"
        self.powersource_name = "none"
        self.voltage = 0


class EventWhois(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:whois"
        self.memcell_name = "none"
        self.mask = 0


class EventFriction(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:friction"
        self.track_name = "none"
        self.friction = 0.5


class EventMultiple(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:multiple"
        self.memcell_name = "none"
        self.events_names = []
        self.else_events_names = []
        self.conditions = Conditions()


class EventSwitch(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:switch"
        self.switch_name = "none"
        self.state = 0
        self.move_rate = -1
        self.move_rate_delay = -1


class EventSound(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:sound"
        self.sound_name = "none"
        self.play_status = 0
        self.radio_channel = 0


class EventDisable(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:disable"


class EventDynvel(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:dynvel"


class EventMessage(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:message"


class EventTexture(Event):
    def __init__(self, name):
        super().__init__(name)
        self.type = "event:texture"
        self.models_names = []
        self.replacableskin_index = 1
        self.material_name = "none"
        self.params_memcell_name = "none"


class Conditions:
    def __init__(self):
        self.use_trackfree = False
        self.use_trackoccupied = False
        self.use_propability = False
        self.use_memcompare = False
        self.memcompare_values = MemcellValues(("*", "*", "*"))

    @property
    def memcompare_values(self):
        return self._memcompare_values

    @memcompare_values.setter
    def memcompare_values(self, values):
        self._memcompare_values = MemcellValues(values)

