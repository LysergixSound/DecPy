import time
import json
import requests
import hashlib

from Models.NeighbourModel import NeighbourModel
from Models.BlockModel import BlockModel
from Models.ResponseModels import ErrorResponseModel
from Models.ResponseModels import SuccessResponseModel
from Models.ResponseModels import InfoResponseModel

def proofOfWork(block, difficulty):
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
def createBlock(address, sender, receiver, expiration, message, difficulty):
        block = BlockModel(hashlib.sha256(sender + message + receiver).hexdigest(), sender, receiver, message, 0, 0, expiration, int(time.time()))
        block = proofOfWork(block, difficulty)
        blockRequest = json.dumps({"method":"setBlock", "block":block.toJSON()})
        send(address, blockRequest)
def send(address, sendData):
        sendHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(address, data=sendData, headers=sendHeaders)
        print response.text


address = "http://192.168.0.61:6962"
createBlock(address, "me", "you", "1m", "hello", 2)