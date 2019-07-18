class SCNEvent:
    def __init__(self, name):
        self.name = "name"
        self.typename = "event"
        self.delay = 0
        self.node_names = []


class SCNEventAddvalues(SCNEvent):
    def __init__(self, name):
        super().__init__()
        self.memcell_name = ""
        self.values = ["*", "*", "*"]
        self.memcell_conditions = {
            
        }