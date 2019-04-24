import json

class NeighbourModel:
    def __init__(self, address = "", alias = ""):
        self.alias = alias
        self.address = address

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)