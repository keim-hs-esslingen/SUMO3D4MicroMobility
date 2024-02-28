import json
import xml.etree.ElementTree as et
import sumolib

from nodesContainer import NodesContainer, Node
from edgesContainer import EdgesContainer, Edge

class ElevationAdder:

    def __init__(self, _filepath, _netFilename, _plainNodesFile, _plainEdgesFile):
        self.filepath = _filepath
        self.netFilename = _netFilename
        self.plainNodesFile = _plainNodesFile
        self.plainEdgesFile = _plainEdgesFile
        self.nodesContainer = NodesContainer()
        self.net = sumolib.net.readNet(self.filepath + self.netFilename)
        self.edgesContainer = EdgesContainer(self.net)

    def addElevations(self):
        self.loadNodes()
        self.requestElevationsForNodes(100)
        self.updateNodesWithElevations()
        self.loadEdges()
        self.requestElevationsForEdges(100)
        self.updateEdgesWithElevations()


    def loadNodes(self):
        print("Load all nodes from XML file ... ", end="")
        tree = et.parse(self.filepath + self.plainNodesFile)
        root = tree.getroot()
        root.findall(".node")

        for element in root.findall(".node"):
            id = element.attrib.get("id")
            y = float(element.attrib.get("y"))
            x = float(element.attrib.get("x"))
            lon, lat = self.net.convertXY2LonLat(x, y)
            node = Node(id, x, y, lat, lon)
            self.nodesContainer.addNode(node)

        print(len(self.nodesContainer.getAllNodes()))

    def loadEdges(self):
        print("Load all edges from XML file ... ", end="")
        tree = et.parse(self.filepath + self.plainEdgesFile)
        root = tree.getroot()
        root.findall(".edge")

        for element in root.findall(".edge"):
            id = element.attrib.get("id")
            if element.attrib.get("shape") != None:
                shape = str(element.attrib.get("shape"))
                edge:Edge = Edge(id, shape)
                edge.createLatLonsWithEle(self.net)
                self.edgesContainer.addEdge(edge)


                #print("shapeArray", edge.shapeArray)
                #print("shapeWithEle", edge.latLonsWithEle)

        print(len(self.edgesContainer.getAllEdges()))
        for edge in self.edgesContainer.getAllEdges():
            #print(edge.getJson())
            pass

    def requestElevationsForNodes(self, _buld_amount):
        print("Request elevations to the founded nodes ... ", end="")
        self.nodesContainer.getElevationsForAllNodes(_buld_amount)

    def requestElevationsForEdges(self, _bulk_amount):
        print("Request elevations to the founded edges ... ", end="")
        self.edgesContainer.getElevationsForAllEdges(_bulk_amount)

    def updateNodesWithElevations(self):
        print("Updating nodes with requested elevations ...", end="")
        tree = et.parse(self.filepath + self.plainNodesFile)
        #print(self.filepath + self.plainNodesFile)
        root = tree.getroot()
        root.findall(".node")

        for element in root.findall(".node"):
            nodeID = element.attrib.get("id")
            node:Node = self.nodesContainer.getNodeByID(nodeID)
            element.set("z", str(round(node.getEle(), 2)))
            #print("Set elevation of node by id " + str(node.getID()) + ": " + str(round(node.getEle(), 2)))

        print(len(self.nodesContainer.getAllNodes()))

        print("Write elevations for nodes to xml file ... ", end="")
        tree.write(self.filepath + self.plainNodesFile)
        print("Done")

    def updateEdgesWithElevations(self):
        print("Updating edges with requested elevations ...", end="")
        tree = et.parse(self.filepath + self.plainEdgesFile)
        #print(self.filepath + self.plainNodesFile)
        root = tree.getroot()
        root.findall("edge")

        for element in root.findall(".edge"):
            if element.attrib.get("shape") != None:
                edgeID = element.attrib.get("id")
                edge:Edge = self.edgesContainer.getEdgeByID(edgeID)
                element.set("shape", str(edge.getShape()))
                #print("Set elevation of node by id " + str(node.getID()) + ": " + str(round(node.getEle(), 2)))


        print(len(self.edgesContainer.getAllEdges()))

        print("Write elevations for edges to xml file ... ", end="")
        tree.write(self.filepath + self.plainEdgesFile)
        print("Done")