import requests
import json
import time

class Node:
    def __init__(self, _id, _x, _y, _lat, _lon):
        self.id= _id
        self.x= _x
        self.y= _y
        self.lat= _lat
        self.lon= _lon
        self.ele = 0.0

    def printID(self): return self.id

    def printX(self): return self.x

    def printY(self): return self.y

    def printLat(self): return self.lat

    def printLon(self): return self.lon

    def printEle(self): return self.ele

    def setEle(self, _ele): self.ele = _ele

    def getLatLonString(self):
        return str(self.lat) + "," + str(self.lon)

    def getID(self):
        return self.id

    def getEle(self):
        return self.ele

    def getJson(self):
        json = {
            "id": self.id, "x": self.x, "y": self.y, "lat": self.lat, "lon": self.lon, "ele": self.ele,
        }
        return json

class NodesContainer:
    def __init__(self):
        self.url = "https://api.opentopodata.org/v1/eudem25m"
        self.nodes = []

    def addNode(self, _node):
        self.nodes.append(_node)

    def getAllNodes(self):
        return self.nodes

    def getNodeByID(self, _id):
        for node in self.nodes:
            if node.getID() == _id:
                return node
        return []

    def print(self):
        for node in self.nodes:
            print(node.getJson())

    def getElevationsForAllNodes(self, _bulk_amount):
        last_index = len(self.nodes) - 1
        print(last_index+1)

        start_index = 0
        end_index = 0
        if (start_index + _bulk_amount - 1) < last_index:
            end_index = start_index + _bulk_amount - 1
        else:
            end_index = last_index

        #print("last_index", last_index)
        #print("_bulk_amount", _bulk_amount)
        #print("start_index", start_index)
        #print("end_index", end_index)
        i = 0
        while i <= last_index:
            #print(" --- ")
            start_index = i

            if (start_index + _bulk_amount - 1) < last_index:
                end_index = start_index + _bulk_amount - 1
            else:
                end_index = last_index

            #print("start_index", start_index)
            #print("end_index", end_index)

            # Added due to the new API limitations
            time.sleep(1)


            data = self.getElevationsForNodes(start_index, end_index)
            print(end_index+1)
            #print(data)
            y = start_index
            while y <= end_index:
                self.nodes[y].setEle(data[y-start_index]["elevation"])
                y = y + 1

            i = i + _bulk_amount
        print(end_index+1)
        #print(self.print())


    def getElevationsForNodes(self, start_index, end_index):
        bulk=[]
        i = start_index

        while i <= end_index:
            bulk.append(self.nodes[i])
            i = i + 1

        return self.requestElevations(bulk)

    def requestElevations(self, _nodes):
        locations = ""
        for node in _nodes:
            locations = locations + node.getLatLonString() + "|"

        locations = locations[:-1]
        data = {
            "locations": locations,
            "interpolation": "cubic",
        }
        #print(data)
        response = requests.post(self.url, data=data)
        result = json.loads(response.content.decode('ascii'))["results"]
        return result