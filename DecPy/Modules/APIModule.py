import time
import json
import requests
import hashlib

from Models.NeighbourModel import NeighbourModel
from Models.BlockModel import BlockModel
from Models.ResponseModels import ErrorResponseModel
from Models.ResponseModels import SuccessResponseModel
from Models.ResponseModels import InfoResponseModel



class Api:
    def __init__(self):
        self.neighbours = []
        self.id = "test 1"
        self.version = "Community Test"
        self.difficulty = 2

    def requestHandler(self, data):
        if "method" in data:
            print data

            # getInfo
            if data["method"] == "getInfo":
                return self.getInfo().toJSON()

            # addNeighbour
            elif data["method"] == "addNeighbour":
                if "address" in data:
                    if self.addNeighbour(data["address"]) == True:
                        return SuccessResponseModel("neighbour added", time.time()).toJSON()
                    else:
                        return ErrorResponseModel("add neighbour failed", time.time()).toJSON()

            # setBlock
            elif data["method"] == "setBlock":
                if "block" in data:
                    if self.setBlock(data["block"]) == True:
                        return SuccessResponseModel("block is valid", time.time()).toJSON()
                    else:
                        return ErrorResponseModel("block is not valid", time.time()).toJSON()

            # getBlock
            elif data["method"] == "getBlock":
                if "block" in data:
                    return self.getBlock(data["block"])

            # testCreateBlock
            elif data["method"] == "createBlock":
                if "sender" in data and "message" in data and "receiver" in data:
                    self.createBlock(data["sender"], data["message"], data["receiver"])
                    return SuccessResponseModel("block created", time.time()).toJSON()


        return ErrorResponseModel("no valid method", time.time()).toJSON()

    def getNeighbourId(self, neighbour):
        return ""
        pass

    def getInfo(self):
        info = InfoResponseModel(self.id, time.time(), self.version)
        return info

    def send(self, neighbour):
        sendHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(neighbour.address, data=sendData, headers=sendHeaders)

    def verifiyData(self, block):
        proofResult = block["blockHash"] + str(block["proof"])
        proofResult = hashlib.sha256(proofResult).hexdigest()

        tempResult = ""
        for x in range(0, block["difficulty"]):
            tempResult = tempResult + "0"

        if proofResult[:block["difficulty"]] == tempResult:
            return True

        return False

    def broadcast(self, sendData):
        sendHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        for neighbour in self.neighbours:
            response = requests.post(neighbour.address, data=sendData, headers=sendHeaders)

    def setBlock(self, block):
        print block
        isValid = self.verifiyData(json.loads(block))
        print isValid
        return isValid

    def saveBlock(self, block):
        pass

    def getBlock(self, block):
        pass

    def pingAll(self):
        self.broadcast('{"method":"getInfo"}')

    def proofOfWork(self, block, difficulty):
        counter = 0
        while True:
            proofResult = block.blockHash + str(counter)
            proofResult = hashlib.sha256(proofResult).hexdigest()

            tempResult = ""
            for x in range(0, difficulty):
                tempResult = tempResult + "0"

            print proofResult[:difficulty]
            if proofResult[:difficulty] == tempResult:
                block.proof = counter
                block.difficulty = difficulty
                break

            counter += 1

        return block

    def createBlock(self, sender, message, receiver):
        block = BlockModel(hashlib.sha256(sender + message + receiver).hexdigest(), sender, message, receiver)
        block = self.proofOfWork(block, self.difficulty)
        blockRequest = json.dumps({"method":"setBlock", "block":block.toJSON()})
        self.broadcast(blockRequest)

    def addNeighbour(self, address):
        try:
            neighbour = NeighbourModel(address)
            if neighbour not in self.neighbours:
                neighbour.id = self.getNeighbourId(neighbour)
                self.neighbours.append(neighbour)

                return True
            else:
                return False
        except:
            return False
