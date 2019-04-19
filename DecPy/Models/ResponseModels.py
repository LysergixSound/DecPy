import json

class InfoResponseModel:
    def __init__(self, id, timestamp, version):
        self.timestamp = timestamp
        self.id = id
        self.version = version

    def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)

class ErrorResponseModel:
    def __init__(self, description, timestamp):
        self.timestamp = timestamp
        self.description = description

    def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)

class SuccessResponseModel:
    def __init__(self, description, timestamp):
        self.timestamp = timestamp
        self.description = description

    def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)