import requests
import json
import sumolib
import time

class Edge:
    def __init__(self, _id, _shape):
        self.id= _id
        self.shape = _shape #"2851.13,2895.78 2867.89,2929.28"
        self.shapeArray = [] #[[2851.13,2895.78,0.0],[2867.89,2929.28,0.0]]"
        self.latLonsWithEle = [] #[[34.2, 32.1, 0.0], [...]
        self.createShapeArray()

    def createShapeArray(self):
        xy = self.shape.split(" ")
        for element in xy:
            x = float(element.split(",")[0])
            y = float(element.split(",")[1])
            ele = 0.0;
            self.shapeArray.append([x, y, ele])

    def createLatLonsWithEle(self, _net):
        xy = self.shape.split(" ")
        for element in xy:
            x = float(element.split(",")[0])
            y = float(element.split(",")[1])
            lon, lat = _net.convertXY2LonLat(x, y)
            self.latLonsWithEle.append([lat, lon, 0])

    def setEvelationDataToShapeArray(self):
        i = 0;
        while i < len(self.latLonsWithEle):
            self.shapeArray[i][2] = round(self.latLonsWithEle[i][2], 2)
            i += 1

    def setElevationsByArray(self, _array):
        for i, element in enumerate(self.latLonsWithEle, start=0):
            for _i, _element in enumerate(_array, start=0):
                if element[0] == _element[0] and element[1] == _element[1]:
                    self.latLonsWithEle[i] = _array[_i]

        self.setEvelationDataToShapeArray()

    def getLatLonsWithEle(self):
        return self.latLonsWithEle

    def getID(self):
        return self.id

    def getJson(self):
        json = {
            "id": self.id, "shape": self.shape,
        }
        return json

    def getJsonWithEle(self):
        json = {
            "id": self.id, "shape": self.shapeArray,
        }
        return json

    def getShape(self):
        shape = "";

        for element in self.shapeArray:
            shape += str(element[0]) + "," + str(element[1]) + "," + str(element[2]) + " "

        shape = shape[:-1]

        return shape

class EdgesContainer:
    def __init__(self, _net):
        self.url = "https://api.opentopodata.org/v1/eudem25m"
        self.net = _net
        self.edges = []
        self.latLons = []

    def addEdge(self, _node):
        self.edges.append(_node)

    def getAllEdges(self):
        return self.edges

    def getEdgeByID(self, _id):
        for edge in self.edges:
            if edge.getID() == _id:
                return edge
        return []

    def print(self):
        for edge in self.edges:
            print(edge.getJson())

    def getElevationsForAllEdges(self, _bulk_amount):
        last_index = len(self.edges) - 1
        print(last_index+1)

        #put all [lat, lons, ele] from the edges into an array
        for edge in self.edges:
            for element in edge.getLatLonsWithEle():
                self.latLons.append(element)

        last_index = len(self.latLons) - 1

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

            data = self.getElevationsForLatLons(start_index,end_index)
            print(end_index+1)
            #print(data)
            y = start_index
            while y <= end_index:
                self.latLons[y][2] = data[y-start_index]["elevation"]
                y = y + 1

            i = i + _bulk_amount
        #Set elevation data to each edge
        for edge in self.edges:
            edge.setElevationsByArray(self.latLons)

        print(end_index+1)

    def getElevationsForLatLons(self, start_index, end_index):
        bulk=[]
        i = start_index

        while i <= end_index:
            bulk.append(self.latLons[i])
            i = i + 1

        return self.requestElevations(bulk)

    def requestElevations(self, _bulk):
        locations = ""
        for element in _bulk:
            locations += str(element[0]) + "," + str(element[1]) + "|"

        locations = locations[:-1]
        data = {
            "locations": locations,
            "interpolation": "cubic",
        }
        #print(data)
        response = requests.post(self.url, data=data)
        result = json.loads(response.content.decode('ascii'))["results"]
        return result