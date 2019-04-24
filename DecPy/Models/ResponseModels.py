import json
import time

class InfoResponseModel:
    def __init__(self, id, version):
        self.timestamp = int(time.time())
        self.id = id
        self.version = version

    def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)

class ErrorResponseModel:
    def __init__(self, description):
        self.timestamp = int(time.time())
        self.description = description

    def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)

class SuccessResponseModel:
    def __init__(self, description):
        self.timestamp = int(time.time())
        self.description = description

    def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)