import json

class BlockModel:
    def __init__(self, blockHash, sender, message, receiver):
        self.blockHash = blockHash
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.proof = 0
        self.difficulty = 0

    def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)
