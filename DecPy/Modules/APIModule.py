import time
import json
import requests
import hashlib
import threading
import mysql.connector

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
        self.sqlDB = mysql.connector.connect(
          host="localhost",
          user="node",
          passwd="hallo243",
          database="statefree"
        )
        self.sqlDataTable = "data"
        self.sqlCursor = self.sqlDB.cursor()

        threading.Thread(target = self.expireThread).start()

    def requestHandler(self, data, rawData):
        if "method" in data:
            print data

            # getInfo
            if data["method"] == "getInfo":
                return self.getInfo().toJSON()

            # addNeighbour
            elif data["method"] == "addNeighbour":
                if "address" in data:
                    return self.addNeighbour(data["address"]).toJSON()

            # setBlock
            elif data["method"] == "setBlock":
                if "block" in data:
                    return self.setBlock(data["block"], rawData).toJSON()

            # getBlockFromHash
            elif data["method"] == "getBlockFromHash":
                if "hash" in data:
                    return json.dumps(self.getBlockFromHash(data["hash"]))

            # getBlocksFromSender
            elif data["method"] == "getBlocksFromSender":
                if "sender" in data:
                    return json.dumps(self.getBlocksFromSender(data["sender"]))

            # getBlocksFromReceiver
            elif data["method"] == "getBlocksFromReceiver":
                if "receiver" in data:
                    return json.dumps(self.getBlocksFromReceiver(data["receiver"]))

        return ErrorResponseModel("no valid method").toJSON()

    def getNeighbourId(self, neighbour):
        return ""
        pass

    def getInfo(self):
        info = InfoResponseModel(self.id, self.version)
        return info

    def send(self, neighbour, sendData):
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
        for neighbour in self.neighbours:
            self.send(neighbour, sendData)

    def setBlock(self, block, rawData):
        blockObj = json.loads(block)
        isValid = self.verifiyData(blockObj)
        if isValid == True:
            if self.saveBlock(blockObj) == True:
                return SuccessResponseModel("block is valid")
            else:
                return ErrorResponseModel("block already exists")
            self.broadcast(rawData)
        else:
            return ErrorResponseModel("block is not valid")

    def saveBlock(self, block):
        sqlQuery = 'SELECT * FROM ' + self.sqlDataTable + ' WHERE blockHash = "' + block["blockHash"] + '"'
        self.sqlCursor.execute(sqlQuery)
        sqlBlocks = self.sqlCursor.fetchall()

        if len(sqlBlocks) == 0:
            vals = '("' + block["blockHash"] + '", "' + block["sender"] + '", "' + block["receiver"] + '", "' + str(block["proof"]) + '", "' + str(block["difficulty"]) + '", "' + block["message"] + '", "' + block["expiration"] + '", "' + str(int(time.time())) + '")'
            sqlQuery = "INSERT INTO " + self.sqlDataTable + " (blockHash, sender, receiver, proof, difficulty, message, expiration, timestamp) VALUES " + vals
            self.sqlCursor.execute(sqlQuery)

            self.sqlDB.commit()
            return True
        else:
            return False

    def getBlockFromHash(self, blockHash):
        sqlQuery = 'SELECT * FROM ' + self.sqlDataTable + ' WHERE blockHash = "' + blockHash + '"'
        self.sqlCursor.execute(sqlQuery)
        sqlBlocks = self.sqlCursor.fetchall()

        blocks = []
        for sqlBlock in sqlBlocks:
            block = BlockModel()
            block.fromSQL(sqlBlock)
            blocks.append(block.toJSON())

        return blocks

    def getBlocksFromSender(self, sender):
        sqlQuery = 'SELECT * FROM ' + self.sqlDataTable + ' WHERE sender = "' + sender + '"'
        self.sqlCursor.execute(sqlQuery)
        sqlBlocks = self.sqlCursor.fetchall()

        blocks = []
        for sqlBlock in sqlBlocks:
            block = BlockModel()
            block.fromSQL(sqlBlock)
            blocks.append(block.toJSON())

        return blocks

    def getBlocksFromReceiver(self, receiver):
        sqlQuery = 'SELECT * FROM ' + self.sqlDataTable + ' WHERE receiver = "' + receiver + '"'
        self.sqlCursor.execute(sqlQuery)
        sqlBlocks = self.sqlCursor.fetchall()

        blocks = []
        for sqlBlock in sqlBlocks:
            block = BlockModel()
            block.fromSQL(sqlBlock)
            blocks.append(block.toJSON())

        return blocks

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

    def expireThread(self):
        while True:
            sqlQuery = 'SELECT * FROM ' + self.sqlDataTable
            self.sqlCursor.execute(sqlQuery)
            sqlBlocks = self.sqlCursor.fetchall()

            print "CHECK EXPIRATION"
            for sqlBlock in sqlBlocks:
                print sqlBlock[7]
                if "m" in sqlBlock[7]:
                    expire = sqlBlock[8] + int(int(sqlBlock[7].replace("m", "")) * 60)
                elif "d" in sqlBlock[7]:
                    expire = sqlBlock[8] + int(int(sqlBlock[7].replace("d", "")) * 24 * 60 * 60)

                print str(expire) + " -- " + str(time.time())
                if expire < time.time():
                    print "DELETE: " + sqlBlock[1]
                    sqlQuery = "DELETE FROM " + self.sqlDataTable + " WHERE blockHash = '" + sqlBlock[1] + "'"
                    self.sqlCursor.execute(sqlQuery)

                    self.sqlDB.commit()


            time.sleep(60)

    def createBlock(self, sender, message, receiver, expiration):
        block = BlockModel(hashlib.sha256(sender + message + receiver).hexdigest(), sender, receiver, message, 0, 0, expiration, int(time.time()))
        block = self.proofOfWork(block, self.difficulty)
        blockRequest = json.dumps({"method":"setBlock", "block":block.toJSON()})
        self.broadcast(blockRequest)

    def addNeighbour(self, address):
        try:
            neighbour = NeighbourModel(address)
            if neighbour not in self.neighbours:
                neighbour.id = self.getNeighbourId(neighbour)
                self.neighbours.append(neighbour)

                return SuccessResponseModel("neighbour added")   
        except:
            pass

        return ErrorResponseModel("add neighbour failed")
