import json

class BlockModel:
    def __init__(self, blockHash = "", sender = "", receiver = "", message = "", proof = 0, difficulty = 0, expiration = "1m", timestamp = 0):
        self.blockHash = blockHash
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.proof = proof
        self.difficulty = difficulty
        self.expiration = expiration
        self.timestamp = timestamp

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromSQL(self, sqlData):
        self.blockHash = sqlData[1]
        self.sender = sqlData[2]
        self.receiver = sqlData[3]
        self.message = sqlData[4]
        self.proof = sqlData[5]
        self.difficulty = sqlData[6]
        self.expiration = sqlData[7]
        self.timestamp = sqlData[8]